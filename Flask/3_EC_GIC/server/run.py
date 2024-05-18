from flask_script import Manager, Server

from server.app import app

manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '127.0.0.1',
    port = 5000)
                    )

if __name__ == "__main__":
    manager.run()

