#!/usr/bin/env ansible-playbook

---
- name: Deploy Full Stack Web Application
  hosts: all
  become: yes
  vars:
    app_name: "myapp"
    web_port: "8080"
    db_name: "mydb"
    app_port: "9999"

  tasks:
    - name: Install Web Server
      pacman:
        name: apache2
        state: present

    - name: Install Database
      pacman:
        name: mysql-server
        state: present

    - name: Configure Web Server
      template:
        src: templates/apache.conf.j2
        dest: /etc/apache2/sites-available/{{ app_name }}.conf
        mode: 0644

    - name: Activate Web Server
      command: a2ensite {{ app_name }}

    - name: Create Database
      mysql_db:
        name: "{{ db_name }}"
        state: present

    - name: Install Application Server
      apt:
        name: gunicorn
        state: present

    - name: Deploy Application
      shell:
        cmd: |
          gunicorn -b 0.0.0.0:{{ app_port }} --pythonpath /var/www/{{ app_name }}/src/ {{ app_name }}.wsgi
