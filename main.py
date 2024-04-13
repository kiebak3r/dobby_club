import secrets
import flet as ft
import sqlite3

# Variables
p_width = 200
current = 1
p_height = 100


def main(page: ft.Page):
    global current

    # Update DB Prompts
    win = ft.TextField(label="Winning Prompt", hint_text="Enter the text to show when user wins")
    lose = ft.TextField(label="Losing Prompt", hint_text="Enter the text to show when user loses")
    dq = ft.TextField(label="Default Questions", hint_text="Enter the amount of questions per game (MAX 7)")
    fqf = ft.TextField(label="Losing Prompt 2", hint_text="Enter the text to show when user fails the first question")

    # Update DB Questions
    q1 = ft.TextField(label="Question1", hint_text="Please enter the question")
    q2 = ft.TextField(label="Question2", hint_text="Please enter the question")
    q3 = ft.TextField(label="Question3", hint_text="Please enter the question")
    q4 = ft.TextField(label="Question4", hint_text="Please enter the question")
    q5 = ft.TextField(label="Question5", hint_text="Please enter the question")
    q6 = ft.TextField(label="Question6", hint_text="Please enter the question")
    q7 = ft.TextField(label="Question7", hint_text="Please enter the question")

    # Update DB Prizes
    p1 = ft.TextField(label="Prize1", hint_text="Please enter the prize")
    p2 = ft.TextField(label="Prize2", hint_text="Please enter the prize")
    p3 = ft.TextField(label="Prize3", hint_text="Please enter the prize")
    p4 = ft.TextField(label="Prize4", hint_text="Please enter the prize")
    p5 = ft.TextField(label="Prize5", hint_text="Please enter the prize")
    p6 = ft.TextField(label="Prize6", hint_text="Please enter the prize")
    p7 = ft.TextField(label="Prize7", hint_text="Please enter the prize")

    # Establish a connection to the SQLite database
    conn = sqlite3.connect('questions.db', check_same_thread=False)
    cursor = conn.cursor()

    def update_db(e):
        # Update questions
        questions = [(q.value, idx) for idx, q in enumerate([q1, q2, q3, q4, q5, q6, q7], start=1) if q.value != ""]
        for value, idx in questions:
            cursor.execute('UPDATE quiz SET question = ? WHERE id = ?', (value, idx))

        # Update prizes
        prizes = [(p.value, idx) for idx, p in enumerate([p1, p2, p3, p4, p5, p6, p7], start=1) if p.value != ""]
        for value, idx in prizes:
            cursor.execute('UPDATE quiz SET prize = ? WHERE id = ?', (value, idx))

        # Update prompts
        if win.value:
            cursor.execute('UPDATE prompts SET win = ?', (win.value,))
        if lose.value:
            cursor.execute('UPDATE prompts SET fail = ?', (lose.value,))
        if fqf.value:
            cursor.execute('UPDATE prompts SET first_question_fail = ?', (fqf.value,))
        if dq.value:
            cursor.execute('UPDATE quiz SET default_prizes = ?', (dq.value,))

        # Commit changes and close connection
        conn.commit()
        conn.close()
        main(page)

    def get_question(idx):
        return cursor.execute(f'SELECT question FROM quiz WHERE id = {idx}').fetchone()[0]

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
        "Bebas": "assets/fonts/BebasNeue-Regular.ttf",
    }
    page.theme = ft.Theme(font_family="Bebas")

    # Prizes UI
    p_count = cursor.execute(f'SELECT default_prizes FROM quiz').fetchone()[0]
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

    def change_questions(e):
        def column_header(text):
            return ft.Text(
                text,
                color='#FF0098',
                size=30,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            )

        page.views[0].controls.clear()
        page.add(
            ft.Row(
                [
                    ft.Column(
                        [
                            column_header('Questions'),
                            q1, q2, q3, q4, q5, q6, q7
                        ],
                        ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Column(
                        [
                            column_header('Prizes'),
                            p1, p2, p3, p4, p5, p6, p7
                        ],
                        ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Column(
                        [
                            column_header('Prompts'),
                            win, lose, fqf, dq
                        ],
                        ft.MainAxisAlignment.START,
                    ),
                    ft.Container(
                        ft.CupertinoButton(
                            content=ft.Text(
                                "Update",
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
                            on_click=update_db,
                        ),
                        alignment=ft.alignment.center,
                    )
                ],
                ft.MainAxisAlignment.CENTER,
            )
        )
        page.update()

    def settings_button():
        prize_list_column.controls.append(ft.Container(ft.TextButton("⚙️", on_click=change_questions)))
        page.update()

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
                    on_click=lambda _: main(page),
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
            question_control.value = cursor.execute(f'SELECT win FROM prompts').fetchone()[0]
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
            settings_button()

    def incorrect_answer(e):
        global current
        for p in prizes:
            if p.src != 'all/correct.png':
                p.src = 'all/incorrect.png'
                p.update()

        if current < 2:
            question_control.value = cursor.execute(f'SELECT first_question_fail FROM prompts').fetchone()[0]
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
                    f" ☠️ 0 Prizes Won ❌",
                    size=20,
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.RED_900,
                    text_align=ft.TextAlign.CENTER,
                )
            )
            play_again()
            settings_button()
            return

        question_control.value = cursor.execute(f'SELECT fail FROM prompts').fetchone()[0]
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
        settings_button()

    def prize_to_bank(idx: int):
        prize_emoji = secrets.choice(['🎁', '💰', '🌟', '🏆', '🎖️', '🔥'])
        response = cursor.execute(f'SELECT prize FROM quiz WHERE id = {idx}').fetchone()[0]
        prize_list_column.controls.append(
            ft.Text(
                f'{prize_emoji}   Prize {current} : {response}   ✅',
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


app = ft.app(target=main, assets_dir='assets')
