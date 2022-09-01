from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.logger.info('listening %s:%s', app.config['HTTP_HOST'], app.config['HTTP_PORT'])
    app.run(app.config['HTTP_HOST'], app.config['HTTP_PORT'], debug=app.config.get('DEBUG', False))