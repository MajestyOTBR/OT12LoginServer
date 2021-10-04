from login_server import LoginServer
from tornado.ioloop import IOLoop
import tornado.web
import json
import models

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, login_server: LoginServer) -> None:
        self.login_server = login_server

    def post(self) -> None:
        try:
            request = json.loads(self.request.body)
            type = request.get("type", "")
            if type == "login":
                email = request.get("email", "")
                password = request.get("password", "")
                if email is None or password is None:
                    return

                self.login_server.process_login(email, password, self)
            elif type == "boostedcreature":
                print("requesting boosted creature")
            elif type == "cacheinfo":
                print("requesting cache info")
            elif type == "eventschedule":
                print("requesting events schedule")
        except Exception as err:
            print(err)

if __name__ == '__main__':
    login_server = LoginServer()
    if not login_server.start():
        print("There was a problem with connecting to database.")
        exit()

    app = tornado.web.Application([(r"/login", MainHandler, dict(login_server=login_server))])

    try:
        app.listen(80)
    except Exception as err:
        print(err)
        exit()

    print("Started listening at {}:{}".format(models.config["host"], models.config["port"]))

    try:
        IOLoop.instance().start()
    except KeyboardInterrupt:
        IOLoop.instance().stop()
