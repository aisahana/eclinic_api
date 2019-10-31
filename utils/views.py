from datetime import datetime

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