if __name__ == '__main__':
    # print("This is not meant to be run by initialzing flask instance")
    # print("Please use gunicorn -w 4 -b (ip):(port) app:app")
    # print("use the any given ip you wish to use")
    # print("change line 179 in route if you wish to change ip and socket")
    from app import app, routes, db
    import sqlalchemy as sa
    import sqlalchemy.orm as so
    from app.models import *


    @app.shell_context_processor
    def make_shell_context():
        return {'sa': sa, 'so': so, 'db': db, 'Booking slots': Booking_slots, 'Seating': Seating}
    app.run(debug=True, host="127.0.0.1", port="8000")
