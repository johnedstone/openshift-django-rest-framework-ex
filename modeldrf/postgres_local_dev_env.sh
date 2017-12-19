# Postgresql local development, not needed for openshift template
unset DATABASE_SERVICE_NAME
unset DATABASE_ENGINE
unset DATABASE_NAME
unset DATABASE_USER
unset DATABASE_PASSWORD

export DATABASE_SERVICE_NAME=postgresql
export DATABASE_ENGINE=postgresql
export DATABASE_NAME=db_name
export DATABASE_USER=db_user
export DATABASE_PASSWORD=db_password
