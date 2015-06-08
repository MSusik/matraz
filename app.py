import os

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from flask.ext.sqlalchemy import SQLAlchemy

from contact import get_contact
from docs import has_docs
from doi import get_doi
from license import get_license
from svg import matraz_svg
from utils import get_repo_info, get_readme


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
socketio = SocketIO(app)


@app.route('/<owner>/<repo>')
def index(owner, repo):
    return render_template('form.html', owner=owner, repo=repo)


@app.route('/<owner>/<repo>/matraz.svg')
def badge(owner, repo):
    current_owner = db.session.query(Owner).filter_by(name=owner).first()
    if current_owner:
        old_repo = Repo.query.filter((Repo.name == repo) |
                                     (Repo.owner_id ==
                                      current_owner.id)).first()
        if old_repo:
            return matraz_svg(old_repo.license, old_repo.contact_info,
                              old_repo.documentation, old_repo.doi)


@socketio.on('get_info', namespace="/badge")
def get_info(message):
    # Message contains repo, owner keys
    owner_name = message["owner"].lower()
    current_owner = db.session.query(Owner).filter_by(name=owner_name).first()
    repo_name = message["repo"].lower()

    if 'refresh' not in message:
        if current_owner:
            current_repo = db.session \
                             .query(Repo)\
                             .filter_by(name=repo_name,
                                        owner_id=current_owner.id).first()
            if current_repo:
                return_message = {
                    "contact": current_repo.contact_info,
                    "license": [current_repo.license,
                                current_repo.license_url],
                    "doi": [current_repo.doi, current_repo.doi_url],
                    "documentation": current_repo.documentation
                }
                emit('info', return_message)
                return

    readme = get_readme(message["owner"], message["repo"])
    repo_info = get_repo_info(message["owner"], message["repo"])
    return_message = {
        "contact": get_contact(message["owner"], message["repo"], repo_info,
                               readme),
        "license": get_license(message["owner"], repo_info),
        "doi": get_doi('https://github.com/%s/%s' % (message["owner"],
                       message["repo"])),
        "documentation": has_docs(message["owner"], message["repo"], readme)
    }

    if current_owner:
        old_repo = Repo.query.filter((Repo.name == repo_name) |
                                     (Repo.owner_id ==
                                      current_owner.id)).first()
        if old_repo:
            db.session.delete(old_repo)

    if not current_owner:
        current_owner = Owner(owner_name)
        db.session.add(current_owner)

    current_repo = Repo(current_owner, repo_name,
                        return_message["documentation"],
                        return_message["doi"][0], return_message["doi"][0],
                        return_message["contact"],
                        return_message["license"][0],
                        return_message["license"][1])
    db.session.add(current_repo)
    db.session.commit()
    emit('info', return_message)


class Owner(db.Model):
    __tablename__ = 'owner'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    repos = db.relationship('Repo', backref='owner')

    def __init__(self, name):
        self.name = name


class Repo(db.Model):
    __tablename__ = 'repo'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))
    name = db.Column(db.String())
    documentation = db.Column(db.Boolean())
    doi = db.Column(db.String())
    doi_url = db.Column(db.String())
    contact_info = db.Column(db.String())
    license = db.Column(db.String())
    license_url = db.Column(db.String())

    def __init__(self, owner, name, docs, doi, doi_url,
                 contact_info, license, license_url):
        self.owner = owner
        self.name = name
        self.documentation = docs
        self.doi = doi
        self.doi_url = doi_url
        self.contact_info = contact_info
        self.license = license
        self.license_url = license_url


if __name__ == '__main__':
    socketio.run(app)
