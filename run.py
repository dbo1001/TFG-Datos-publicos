from web import app


# Carga el archuvo de configuración
app.config.from_object('config.Config')


if __name__ == '__main__':
    app.run()
