import data
import sys
import moviesystem

# 예매 기능
def reserve(user_id):
    # 상영 스케쥴 출력
    schedule_list = data.get_schedule_list()
    schedule_list = sort_schedule(schedule_list, "20240404", "04:04")
    [ movie_list, theater_list, seat_list, ticket_list, reservation_list ] = get_lists()

    table = get_schedule_table(schedule_list, movie_list, theater_list, seat_list, ticket_list, reservation_list)
    print_schedule_list(table)

    # 예매할 영화 번호 입력
    while True:
        print("예매할 시간표 아이디를 입력해주세요")
        choice = input("시간표아이디 입력 : ")
        if validate_input(choice):
            if is_id_exist(table, choice): # 가능한 시간표 아이디 범위 내이면
                if if_seat_full(table, choice): # 여석이 모자르면(매진이면)
                    print("여석이 없습니다")
                else: # 정상 입력 + 여석 존재면
                    break
                # 좌석 출력
            else: # 그 밖의 범위이면
                print("영화가 존재하지 않습니다")
        else: # 문법적으로 올바르지 않을 때
            print("시간표아이디는 숫자로 이루어진 길이가 1 이상인 문자열입니다.")
    

    schedule = get_schedule(choice, schedule_list)
    tickets = get_tickets(schedule, seat_list, ticket_list)
    seats = get_ticket_reservation_map(tickets, reservation_list)
    print_seats(seats)

    while True:
        print("예약인원수를 입력해주세요")
        choice = input("예약인원수 입력: ")
        if validate_seat_choice(choice): # 문법이 맞은 경우
            if check_maximum_inline(choice, seats):
                break
            else:  # 예약인원수를 만족하는 연속으로 배치된 좌석이 부족
                print("예약인원수를 만족하는 연속으로 배치된 좌석이 부족합니다.")
        else:
            print("예약인원수는 1~5 사이 숫자로 이루어진 길이가 1인 문자열입니다.")
   
    people = choice

    while True:
        print("예매할 좌석번호를 입력해주세요")
        print("(좌석번호를 기준으로 오른쪽 방향으로 예약인원수 만큼 예매를 진행합니다.)")
        choice = input("좌석번호 입력: ")
        if validate_seat_number(choice): # 문법이 맞은 경우
            if check_seat_available(choice, seats, people): # 오른쪽으로 예약인원수만큼 부족하거나 이미 예약된 좌석인 경우
                break
            else:
                print("예약이 불가능한 좌석입니다.")
        else: # 문법 규칙에 부합하지 않는 경우
            print("올바른 좌석번호를 입력해 주시기 바랍니다.")
    
    make_reservation(reservation_list, user_id, choice, people, tickets)
    print("예매가 완료되었습니다")



### reserve 짜잘이 함수들 ###

def sort_schedule(schedule_list, date, time):
    schedule_list = sorted(schedule_list,key=lambda x:x[3]+x[4])
    print(schedule_list)
    idx = -1
    length = len(schedule_list)
    for i in range(length):
        date1 = schedule_list[i][3]
        time1 = schedule_list[i][4]
        if date+time < date1+time1:
            idx = i
            break
    if idx == -1:
        return []
    else:
        return schedule_list[idx:length]

# 테이블 긁어오기
def get_lists():
    movie_list = data.get_movie_list()
    theater_list = data.get_theater_list()
    seat_list = data.get_seat_list()
    ticket_list = data.get_ticket_list()
    reservation_list = data.get_reservation_list()

    return [movie_list, theater_list, seat_list, ticket_list, reservation_list]

# 스케쥴 테이블 구성(join 연산)
def get_schedule_table(schedule_list, movie_list, theater_list, seat_list, ticket_list, reservation_list):
    table = []
    for i in range(len(schedule_list)):
        (id, movie_id, theater_id, date, time) = schedule_list[i]
        movie_title = find_movie(movie_list, movie_id)[1]
        theater_name = find_theater(theater_list, theater_id)[1]
        max = get_maximum(theater_id, seat_list)
        cur = get_current(id, ticket_list, reservation_list)
        start_time = time.split("-")[0].strip()
        end_time = time.split("-")[1].strip()
        table.append([id, movie_title, date, start_time, end_time, cur, max, theater_name])

    return table

def find_movie(movie_list, id):
    for movie in movie_list:
        if movie[0] == id:
            return movie
    return None

def find_theater(theater_list, id):
    for theater in theater_list:
        if theater[0] == id:
            return theater
    return None

# 해당하는 스케쥴의 최대 정원 구하기
# 해당하는 스케쥴의 상영관의 seat 수
def get_maximum(theater_id, seat_list):
    count = 0
    for seat in seat_list:
        if seat[1] == theater_id:
            count = count + 1
    return count

# 해당하는 스케쥴의 에약된 seat의 수
# 해당하는 스케쥴의 티켓
def get_current(schedule_id, ticket_list, reservation_list):
    cur_tickets = []
    for ticket in ticket_list:
        if ticket[3] == schedule_id:
            cur_tickets.append(ticket)
            
    count = 0
    for reservation in reservation_list:
        if reservation[3] == True:
            continue
        for ticket in cur_tickets:
            if ticket[1] == reservation[0]:
                count = count + 1
    
    return count

# 스케쥴 표 출력
def print_schedule_list(table):
    print("영화목록")
    print("시간표아이디\t영화제목\t날짜/상영시간\t예약인원/최대예약인원\t상영관")
    for (id, movie_title, date, start_time, end_time, cur, max, theater_name) in table:
        print(str(id)+"\t\t"+movie_title+"\t\t"+date+"/"+start_time+"-"+end_time+"\t"+str(cur)+"/"+str(max)+"\t\t"+theater_name)
    # 영화목록
    # 시간표아이디 영화제목  날짜/상영시간     예약인원/최대예약인원   상영관
    #     1      파묘   04.04/08-10        25 / 25명       1관

def validate_input(choice):
    # 문법적 형식 검증
    if len(choice) < 1 or not choice.isdigit():
        #print("validate_date_syntax error")
        return False
    return True

def is_id_exist(table, id):
    for schedule in table:
        if schedule[0] == id:
            return True
    return False

def if_seat_full(table, id):
    for schedule in table:
        if schedule[0] == id:
            if int(schedule[5]) >= int(schedule[6]):
                return True
    return False

def get_schedule(schedule_id, schedule_list):
    for schedule in schedule_list:
        if schedule[0] == schedule_id:
            return schedule

# 해당 스케쥴의 좌석 목록과 좌석 예약 상태 불러오기
def get_tickets(schedule, seat_list, ticket_list):
    (id, theater_id, movie_id, date, time) = schedule
    
    tickets = []
    for ticket in ticket_list:
        if ticket[3] == id:
            tickets.append(ticket)

    tickets = sort_tickets(tickets, seat_list)
    return tickets

def sort_tickets(tickets, seat_list):
    map = []
    for ticket in tickets:
        for seat in seat_list:
            if ticket[2] == seat[0]:
                temp = ticket + [seat[2]]
                map.append(temp)
    sorted_map = sorted(map, key=lambda x:x[4])
    ret = []
    for t in sorted_map:
        ret.append(t)

    return ret

def get_ticket_reservation_map(tickets, reservation_list):
    ret = []
    for i in range(len(tickets)):
        ret.append(tickets[i] + ['O'])

    for i in range(len(tickets)):
        ticket = tickets[i]
        for reservation in reservation_list:
            if ticket[1] == reservation[0]:
                if reservation[3] == 'X':
                    ret[i][5] = 'X'

    return ret


def print_seats(seats):
    alphabet = ['A', 'B', 'C', 'D', 'E']

    print("좌석 입력")
    print("  | 0 1 2 3 4")
    print("  -----------")

    j = 0
    str = ""
    for i in range(len(seats)):
        if i % 5 == 0:
            str = ""
            str = str + alphabet[j] + " |"
            j = j+1
        str = str + " " + seats[i][5]
        if i % 5 == 4:
            str = str + "\n"
            print(str)
    # 좌석 입력
    # 좌석 출력
    #   | 0 1 2 3 4
    #   -----------
    # A | X O X O X
    # B | X O X O X 

def validate_seat_choice(choice):
    if not choice.isdigit():
        return False
    if (int(choice) < 1 or int(choice) > 5) or len(choice) != 1:
        return False
    return True

def check_maximum_inline(choice, seats):
    max = 0
    cur = 0
    local_max = 0
    for i in range(len(seats)):
        if seats[i][5] == 'O':
            cur = cur + 1
        else:
            if local_max < cur:
                local_max = cur
            cur = 0
        
        if i%5 == 4:
            if local_max < cur:
                local_max = cur
            cur = 0

            if max < local_max:
                max = local_max
            local_max = 0
            
    return int(choice) <= max

def validate_seat_number(choice):
    row = choice[0]
    column = choice[1]

    if not ('A' <= row and row <= 'E'):
        return False
    if not column.isdigit() or int(column) < 1 or 5 < int(column):
        return False
    return True

def check_seat_available(choice, seats, people):
    row = choice[0]
    row = (ord(row) - ord('A')) * 5
    column = int(choice[1])
    people = int(people)

    if 4 - column + 1 < people:
        return False
    
    for i in range(people):
        idx = row + column + i
        if seats[idx][5] == 'X':
            return False

    return True

def make_reservation(reservation_list, user_id, choice, people, tickets):
    row = choice[0]
    row = (ord(row) - ord('A')) * 5
    column = int(choice[1])
    people = int(people)

    ticket_ids = []
    for i in range(people):
        idx = row + column + i
        ticket_ids.append(tickets[idx][0])
    
    if reservation_list == []:
        reservation_id = 1
    else:
        reservation_id = int(reservation_list[-1][0]) + 1

    data.add_reservation(str(reservation_id), str(user_id), str(people), 'X')
    edit_ticket_reservation(ticket_ids, reservation_id)


def edit_ticket_reservation(ticket_id_list, reservation_id):
    ticket_list = data.get_ticket_list()  # 기존 영화 목록을 읽어옴

    # 티켓을 수정할 대상의 인덱스를 찾음
    for a, (id, reservation_id1, seat_id, schedule_id) in enumerate(ticket_list):
        for ticket_id in ticket_id_list:
            if ticket_id == id:
                ticket_list[a] = (id, reservation_id, seat_id, schedule_id)  # 새로운 예약 아이디로 수정

    # 수정된 내용을 파일에 기록
    with open("data/" + "ticket.txt", 'w', encoding='utf-8') as f:
        for id, reservation_id1, seat_id, schedule_id in ticket_list:
            f.write(f"{id}/{reservation_id1}/{seat_id}/{schedule_id}\n")