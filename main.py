import secrets
import flet as ft
import firebase_admin
from firebase_admin import credentials, db

# Variables
p_width = 200
current = 1
p_height = 100


cred = credentials.Certificate("assets/all/creds.json")
firebase_admin.initialize_app(
    cred, {
        'databaseURL': 'https://dobby-club-c17d8-default-rtdb.europe-west1.firebasedatabase.app/'
    }
)


def main(page: ft.Page):
    global current

    def get_question(idx):
        return db.reference(f'/db/quiz/{idx}/question').get()

    # Page Configurations
    page.title = "Dobby Club"
    page.window_always_on_top = True
    page.theme_mode = "dark"
    page.window_min_width = 1920
    page.window_min_height = 1080
    page.window_bgcolor = ft.colors.BLACK
    page.window_icon = "assets/favicon.png"

    # Theming
    page.fonts = {
        "Bebas": "assets/all/BebasNeue-Regular.ttf",
    }
    page.theme = ft.Theme(font_family="Bebas")

    # Prizes UI
    p_count = db.reference('/db/quiz/default_prizes').get()
    p_images = ['all/prize.png' for _ in range(int(p_count))]
    prizes = [ft.Image(src=i, fit=ft.ImageFit.CONTAIN, width=p_width, height=p_height) for i in p_images]
    prizes_column = ft.Column(prizes, alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    # Question UI
    question_control = ft.Text(
        get_question(1),
        size=40,
        style=ft.TextThemeStyle.TITLE_LARGE,
        color=ft.colors.WHITE,
        bgcolor='#FF0098',
        weight=ft.FontWeight.BOLD,
        italic=True,
        text_align=ft.TextAlign.CENTER,
    )

    # Winning meme UI
    meme_column = ft.Column(
        controls=[],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    question_column = ft.Container(question_control, alignment=ft.alignment.center)

    # Prize List UI
    prize_list_column = ft.Column(
        [],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    def play_again():
        prize_list_column.controls.append(
            ft.Container(
                ft.CupertinoButton(
                    content=ft.Text(
                        "Play Again?",
                        color=ft.colors.WHITE,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        font_family="Bebas",
                    ),
                    bgcolor='#FF0098',
                    alignment=ft.alignment.top_left,
                    border_radius=ft.border_radius.all(15),
                    opacity_on_click=0.5,
                    on_click=lambda e: main(page),
                ),
                alignment=ft.alignment.center,
            )
        )
        incorrect_button.visible = False
        correct_button.visible = False
        page.update()

    # Bank UI with Prizes
    bank_column = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Image(src='all/bank.png', width=100, height=100),
                    ],
                ),
                prize_list_column
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding(10, 10, 10, 10),
    )

    def correct_answer(e):
        global current
        question_control.value = get_question(current + 1)
        question_control.update()
        index = len(prizes) - current

        if index < len(prizes):
            prizes[index].src = 'all/correct.png'
            prizes[index].update()
            prize_to_bank(current)
        current += 1

        if current > len(prizes):
            question_control.value = db.reference('/db/prompts/win').get()
            question_control.update()
            meme_column.controls.append(
                ft.Container(
                    ft.Image(
                        src='all/win.png',
                        width=400,
                        height=200,
                    ),
                    alignment=ft.alignment.center,
                )
            )
            play_again()

    def incorrect_answer(e):
        global current
        for p in prizes:
            if p.src != 'all/correct.png':
                p.src = 'all/incorrect.png'
                p.update()

        if current < 2:
            question_control.value = db.reference('/db/prompts/first_question_fail').get()
            meme_column.controls.append(
                ft.Container(
                    ft.Image(
                        src='all/first_question_fail.png',
                        width=400,
                        height=200,
                    ),
                    alignment=ft.alignment.center,
                )
            )
            prize_list_column.controls.append(
                ft.Text(
                    f"Game Over : 0 Prizes Won",
                    size=20,
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.RED_900,
                    text_align=ft.TextAlign.CENTER,
                )
            )
            play_again()
            return

        question_control.value = db.reference('/db/prompts/fail').get()
        meme_column.controls.append(
            ft.Container(
                ft.Image(
                    src='all/wrong_answer_meme.png',
                    width=400,
                    height=200,
                ),
                alignment=ft.alignment.center,
            )
        )
        play_again()

    def prize_to_bank(idx: int):
        prize_emoji = secrets.choice(['🎁', '💰', '🌟', '🏆', '🎖️', '🔥'])
        response = db.reference(f'/db/quiz/{idx}/prize').get()
        prize_list_column.controls.append(
            ft.Text(
                f'{prize_emoji}   Prize {current} : {response}   ✔️',
                size=20,
                color=ft.colors.WHITE,
                bgcolor=ft.colors.GREEN,
            )
        )
        prize_list_column.update()

    incorrect_button = ft.IconButton(
        icon=ft.icons.CLOSE,
        icon_color=ft.colors.RED,
        on_click=incorrect_answer,
        icon_size=50,
    )

    correct_button = ft.IconButton(
        icon=ft.icons.CHECK,
        icon_color=ft.colors.GREEN,
        on_click=correct_answer,
        icon_size=50,
    )

    # Main UI layout
    main_content = ft.Row(
        [
            prizes_column,
            ft.Container(
                ft.Column(
                    [
                        meme_column,
                        question_column,
                        ft.Row(
                            [
                                incorrect_button,
                                correct_button,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Divider(opacity=0),
                        ft.Divider(opacity=0),
                        ft.Divider(opacity=0),
                    ],
                    scroll=ft.ScrollMode.HIDDEN,
                ),
                expand=True,
                alignment=ft.alignment.bottom_center,
            ),
            bank_column,
            ft.VerticalDivider(opacity=0),
        ],
        expand=True,
    )
    main_body = ft.Container(
        main_content,
        expand=True,
        image_src='all/bg.png',
        image_fit=ft.ImageFit.COVER,
        image_opacity=0.8,
        border_radius=ft.BorderRadius(5, 5, 5, 5),
    )

    current = 1
    page.views[0].controls.clear()
    page.views[0].controls.append(main_body)
    page.update()


app = ft.app(target=main, assets_dir='assets', export_asgi_app=True, port=8502)
