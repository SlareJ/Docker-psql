import psycopg2
from random import choice
from string import ascii_letters


def check_tinyurl(tiny_link):
    cursor.execute(f"select tinyurl from links where tinyurl = '{tiny_link}'")
    lnk = cursor.fetchone()
    return tiny_link if lnk is None else check_tinyurl(get_tinyurl())


def check_input(link):
    if link in ''' \"\'''':
        return Exception, True
    for el in link:
        if el in ''' \" \'''':
            return Exception, True
    cursor.execute(f"select tinyurl from links where url = '{link}';")
    lnk = cursor.fetchone()
    return (lnk[0], True) if lnk else (get_tinyurl(), False)


def get_tinyurl():
    str = ascii_letters + "0123456789"
    lst = [choice(str) for _ in range(7)]
    return "".join(lst)


conn = psycopg2.connect(dbname='habrdb', user='habrpguser',
                        password='pgpwd4habr', host='localhost')
cursor = conn.cursor()


def tiny(long_link):
    tiny_url, flag = check_input(long_link)
    if flag:
        return tiny_url
    else:
        tiny_url = check_tinyurl(tiny_url)
        cursor.execute(f"insert into links (url, tinyurl) values ('{long_link}', '{tiny_url}')")
        conn.commit()
        return tiny_url


def long(tiny_link):
    if tiny_link in ''' \"\'''':
        return None
    for el in tiny_link:
        if el in ''' \"\'''':
            return None
    cursor.execute(f"select url from links where tinyurl = '{tiny_link}'")
    long = cursor.fetchone()
    if long is not None:
        return long[0]

if __name__ == "__main__":
    tiny_link = input()
    print(long(tiny_link))



