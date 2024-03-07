import psycopg2


def create_db(conn):
	with conn.cursor() as cur:
		cur.execute("""
			CREATE TABLE  IF NOT EXISTS users(
			user_id SERIAL PRIMARY KEY,
			first_name VARCHAR(40) NOT NULL,
			last_name VARCHAR(40) NOT NULL,
			email VARCHAR(80) UNIQUE NOT NULL,
			CHECK(email LIKE '%@%' AND email LIKE '%.%')
			);
		""")
		cur.execute("""
			CREATE TABLE IF NOT EXISTS phones(
			phone_id SERIAL PRIMARY KEY,
			user_id SERIAL REFERENCES users(user_id),
			phone VARCHAR(20) UNIQUE NOT NULL CHECK(phone LIKE '+7__________' OR phone LIKE '8__________')
			);
		""")


def add_user(conn, first_name, last_name, email, phone=None):
	with conn.cursor() as cur:
		cur.execute("""
			INSERT INTO users(first_name, last_name, email) 
			VALUES (%s, %s, %s) 
			RETURNING user_id, first_name, last_name, email;
		""", (first_name, last_name, email))
		print(cur.fetchone())


def add_phone(conn, user_id, phone):
	with conn.cursor() as cur:
		cur.execute("""
			INSERT INTO phones(user_id, phone) 
			VALUES(%s, %s) 
			RETURNING phone_id;
		""", (user_id, phone))
		print(f'User id_{user_id} add {phone} ')


def change_user(conn, user_id, first_name=None, last_name=None, email=None, phone=None):
	with conn.cursor() as cur:
		if first_name is not None:
			cur.execute("""
				UPDATE users
				SET first_name=%s
				WHERE user_id=%s;
			""", (first_name, user_id))
		else:
			pass
		if last_name is not None:
			cur.execute("""
				UPDATE users
				SET last_name=%s
				WHERE user_id=%s;	
			""", (last_name, user_id))
		else:
			pass
		if email is not None:
			cur.execute("""
				UPDATE users
				SET email=%s
				WHERE user_id=%s;
			""", (email, user_id))
		else:
			pass
		print(f'User id_{user_id} change info')


def delete_phone(conn, user_id, phone):
	with conn.cursor() as cur:
		cur.execute("""
			DELETE FROM phones 
			WHERE user_id=%s AND phone=%s;
		""", (user_id, phone,))
		print(f'User id_{user_id} delete {phone}')


def delete_user(conn, user_id):
	with conn.cursor() as cur:
		cur.execute("""
			DELETE FROM phones WHERE user_id=%s;
		""", (user_id,))
		cur.execute("""
			DELETE FROM users WHERE user_id=%s;
		""", (user_id,))
		print(f'User id_{user_id} delete')


def find_user(conn, first_name=None, last_name=None, email=None, phone=None):
	with conn.cursor() as cur:
		if (first_name or last_name or email or phone) is not None:
			cur.execute("""
			SELECT users.user_id, first_name, last_name, email, phone
			FROM users
			LEFT JOIN phones ON users.user_id = phones.user_id
			WHERE first_name=%s OR last_name=%s OR email=%s OR phone=%s;
			""", (first_name, last_name, email, phone))
			result = cur.fetchall()
			for r in result:
				print(f'User id_{r[0]} {r[1]} {r[2]} {r[3]} {r[4]} found')
		else:
			pass


with psycopg2.connect(database="DBHomework_3", user="postgres", password="admin") as conn:
	create_db(conn)

	add_user(conn, "Ivan", "Ivanov", "Ivanov@ya.ru")
	add_user(conn, "Ivan", "Smirnov", "Smirnov@ya.ru")
	add_user(conn, "Petr", "Petrov", "Petrov@ya.ru")
	add_user(conn, "Sidor", "Sidorov", "Sidorov@ya.ru")
	add_user(conn, "Fedor", "Fedorov", "Fedorov@ya.ru")
	add_user(conn, "Egor", "Egorov", "Egorov@ya.ru")
	add_user(conn, "Alex", "Alexeev", "Alexeev@ya.ru")

	add_phone(conn, 1, "+79999999977")
	add_phone(conn, 1, "+79999999988")
	add_phone(conn, 1, "+79999999999")
	add_phone(conn, 2, "+79999999966")
	add_phone(conn, 2, "+79999999955")
	add_phone(conn, 3, "+79999999944")
	add_phone(conn, 5, "+79999999933")

	change_user(conn, 1, first_name="Иван", email="Ivanov1993@ya.ru")
	change_user(conn, user_id=2, last_name="Смирнов")

	delete_phone(conn, 1, "+79999999999")
	delete_user(conn, 3)

	find_user(conn, phone="+79999999933")
	find_user(conn, first_name="Egor")
	find_user(conn, email="Ivanov1993@ya.ru")

conn.close()
