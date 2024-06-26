# theater
def add_theater(id, name, seat):
    file_a("theater.txt", id + '/' + name + '/' + seat + '\n')


def get_theater_list():
    theater_list = file_r("theater.txt")
    return theater_list


# seat
def add_seat(seat_id, theater_id, seat_num):
    file_a("seat.txt", seat_id + '/' + theater_id + '/' + seat_num + '\n')


def get_seat_list():
    seat_list = file_r("seat.txt")
    return seat_list


# movie
def add_movie(id, name, time):
    file_a("movie.txt", id + '/' + name + '/' + str(time) + '\n')


def get_movie_list():
    movie_list = file_r("movie.txt")
    return movie_list


# schedule
def add_schedule(timetable_id, movie_id, theater_id, date, time):
    file_a("schedule.txt", timetable_id + '/' + movie_id + '/' + theater_id + '/' + date + '/' + time + '\n')


def get_schedule_list():
    schedule_list = file_r("schedule.txt")
    return schedule_list


# ticket
def add_ticket(ticket_id, reservation_id, seat_id, timetable_id, ticket_price):
    file_a("ticket.txt",
           ticket_id + '/' + reservation_id + '/' + seat_id + '/' + timetable_id + '/' + ticket_price + '\n')


def get_ticket_list():
    ticket_list = file_r("ticket.txt")
    return ticket_list


def get_ticket_list2():  # chrin2 // 0 : 티켓아이디 1:예매아이디 2:좌석아이디 3:시간표아이디 4:티켓가격
    ticket_list = []
    file = file_r("ticket.txt")
    for ticket_id, reservation_id, seat_id, timetable_id, ticket_price in file:
        ticket_list.append([ticket_id, reservation_id, seat_id, timetable_id, ticket_price])
    return ticket_list


# reservation
def add_reservation(reservation_id, user_id, num, cancel, coupon_price):
    file_a("reservation.txt", reservation_id + '/' + user_id + '/' + num + '/' + cancel + '/' + coupon_price + '\n')


def get_reservation_list():
    ticket_list = file_r("reservation.txt")
    return ticket_list


def get_reservation_list2():  # chrin2 // 0 : 예매아이디 1:예약자아이디 2: 예약인원수 3: 예약취소여부 4: 적용쿠폰가격
    reservation_list = []
    file = file_r("reservation.txt")
    for reservation_id, user_id, num, cancel, coupon_price in file:
        reservation_list.append([reservation_id, user_id, num, cancel, coupon_price])
    return reservation_list


# user
def add_user(user_id, coupon_price, coupon_available):
    file_a("user.txt", user_id + '/' + coupon_price + '/' + coupon_available + '\n')


def get_user_list():
    user_list = file_r("user.txt")
    return user_list


def get_user_list2():  # chrin2 //0 : user_id, 1 :  coupon_price, 2 : coupon_available
    user_list = []
    file = file_r("user.txt")
    for user_id, coupon_price, coupon_available in file:
        user_list.append([user_id, coupon_price, coupon_available])
    return user_list


def get_movie_from_ticket(reservation_id):
    # 예매 id를 통해 해당 영화 id 반환 | in_t: ticket_list에서 가져온 변수 | in_s:schedule_list에서 가져온 변수
    ticket_list = get_ticket_list()
    schedule_list = get_schedule_list()

    for _, reservation_id_in_t, _, schedule_id_in_t, _ in ticket_list:
        if reservation_id_in_t == reservation_id:
            for schedule_id_in_s, _, movie_id_in_s, _, _ in schedule_list:
                if schedule_id_in_s == schedule_id_in_t:
                    return movie_id_in_s


def get_seat_from_ticket(reservation_id):
    # 예매 id를 통해 해당 좌석 id 반환 | in_t: ticket_list에서 가져온 변수 | in_s:schedule_list에서 가져온 변수
    ticket_list = get_ticket_list()

    for _, reservation_id_in_t, seat_id_in_t, schedule_id_in_t, _ in ticket_list:
        if reservation_id_in_t == reservation_id:
            return seat_id_in_t


def file_a(path, content):
    f = open("data/" + path, 'a', encoding='utf-8')
    f.write(content)
    f.close()


def file_i(path, content):
    f = open("data/" + path, 'w', encoding='utf-8')
    f.write(content)
    f.close()


def file_r(path):
    f = open("data/" + path, 'r', encoding='utf-8')
    data_list = f.readlines()
    f.close()
    return data_parsing(data_list)


def file_r_no_strip(path):
    f = open("data/" + path, 'r', encoding='utf-8')
    data_list = f.readlines()
    f.close()
    return data_parsing_no_strip(data_list)


# base function
def data_parsing(array):
    parsed_data = []
    for str in array:
        row = str.strip().split('/')
        parsed_data.append(row)
    return parsed_data


# base function
def data_parsing_no_strip(array):
    parsed_data = []
    for str in array:
        row = str.split('/')
        parsed_data.append(row)
    return parsed_data


def sort_data(data_list, index):
    return sorted(data_list, key=lambda x: x[index])
