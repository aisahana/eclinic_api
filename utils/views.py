from datetime import datetime, date

from counters.models import Queue


def pdf_template(body, title, orientation='potrait', subject='Laporan'):
    return {
        'pageSize': 'A4',
        'pageMargins': [40, 60, 40, 60],
        'pageOrientation': orientation,
        'watermark': {
            'text': 'Aisahana eClinic',
            'color': '#a39b91',
            'opacity': 0.3,
            'bold': True,
            'italics': False,
            'fontSize': 55
        },
        'info': {
            'title': 'Aisahana Reporting',
            'author': 'Aisahana',
            'subject': subject,
        },
        'content': [
            {'text': title, 'style': 'header'},
            {'text': f'Dibuat pada {datetime.now().strftime("%d/%m/%Y")}'},
            '\n',
            *body,
        ],
        'styles': {
            'header': {
                'fontSize': 18,
                'bold': True,
                'color': '#2e65d4',
                'margin': [0, 0, 0, 10]
            },
            'subheader': {
                'fontSize': 16,
                'bold': True,
                'margin': [0, 10, 0, 5]
            },
            'tableHeader': {
                'bold': True,
                'fontSize': 13,
                'color': 'black'
            }
        },
    }


def calculate_age(born):
    print(type(born))
    if not born:
        return 0
    today = date.today()
    try:
        birthday = born.replace(year=today.year)
    except ValueError:
        birthday = born.replace(year=today.year,
                                month=born.month + 1, day=1)

    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year


def generate_queue(counter, que):
    q = Queue.objects.filter(
        counter=counter,
        codec_time=datetime.now().date(),
        is_draft=False
    ).exclude(pk=que.pk).count()

    queue = que
    queue.counter=counter
    queue.codec_time=datetime.now().date()
    queue.is_draft=False
    queue.number=q+1
    queue.save()

    return queue
