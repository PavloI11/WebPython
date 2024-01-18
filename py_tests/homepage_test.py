from flask import url_for

def test_main_page_view(client):
    response = client.get(url_for('home_bp.index'))
    assert response.status_code == 200
    assert u"Ласкаво просимо" in response.data.decode('utf8')

def test_about_view(client):
    response = client.get(url_for('home_bp.about'))
    assert response.status_code == 200
    assert u"PostgreSQL" in response.data.decode('utf8')

def test_projects_view(client):
    response = client.get(url_for('home_bp.projects'))
    assert response.status_code == 200
    assert u"проекти" in response.data.decode('utf8')

def test_contact_view(client):
    response = client.get(url_for('home_bp.contact'))
    assert response.status_code == 200
    assert u"запити" in response.data.decode('utf8')