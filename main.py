import flet as ft
import asyncio

# Variables
p_width = 200
current = 1
seconds = int
p_height = 100
current_beers = 0
first_prize_instance = 1
current_prizes = []


async def main(page: ft.Page):
    global current, seconds, current_beers, first_prize_instance
    current_beers = 0
    seconds = 150
    first_prize_instance = 1
    current_prizes.clear()

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

    p_images = ['all/prize.png' for _ in range(int(6))]
    prizes = [ft.Image(src=i, fit=ft.ImageFit.CONTAIN, width=p_width, height=p_height) for i in p_images]
    prizes_column = ft.Column(prizes, alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    # Countdown UI
    countdown = ft.Text(
        "",
        size=200,
        style=ft.TextThemeStyle.TITLE_LARGE,
        color=ft.colors.WHITE,
        weight=ft.FontWeight.BOLD,
        italic=True,
        text_align=ft.TextAlign.CENTER,
    )
    countdown_column = ft.Container(countdown, alignment=ft.alignment.center)

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
                        "NEXT ROUND",
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
                    on_click=restart,
                ),
                alignment=ft.alignment.center,
            )
        )
        incorrect_button.visible = False
        correct_button.visible = False
        bank.visible = False
        page.update()

    async def restart(e):
        await main(page)

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
        global current, current_beers
        index = len(prizes) - current
        if index < len(prizes):
            prizes[index].src = f'all/beer{index}.png'
            prizes[index].update()
            current_beers += 1
        current += 1

        if current > len(prizes):
            global seconds
            seconds = 0
            prize_to_bank(e)

        button_row.controls.append(bank)
        bank.visible = True
        page.update()

    def incorrect_answer(e):
        global current, current_beers
        for i in range(len(prizes)):
            prizes[i].src = 'all/prize.png'
            prizes[i].update()
        current = 1
        current_beers = 0
        bank.visible = False
        button_row.update()

    async def start_timer(e):
        global seconds
        start.visible = False
        button_row.controls.append(incorrect_button)
        button_row.controls.append(correct_button)
        button_row.update()

        while seconds > 0:
            minutes = seconds // 60
            remaining_seconds = seconds % 60

            countdown.value = "{:2d}:{:02d}".format(minutes, remaining_seconds)
            countdown.update()
            await asyncio.sleep(1)
            seconds -= 1

            if seconds <= 75:
                countdown.color = ft.colors.AMBER
                countdown.update()

            if seconds <= 30:
                countdown.color = ft.colors.RED
                countdown.update()

        countdown.value = ""
        countdown.update()
        play_again()

    def prize_to_bank(e):
        global first_prize_instance, current_beers
        current_prizes.append(current_beers) if current_beers > 0 else None
        current_beers = 0
        prompt = '🍺'

        beers = ft.Text(f'{current_prizes[0]} {prompt}', size=40, color=ft.colors.WHITE)
        if first_prize_instance >= 2:
            beers.value = f'{sum(current_prizes)} {prompt}'
            prize_list_column.controls[-1] = beers

        if first_prize_instance < 2:
            prize_list_column.controls.append(beers)
            first_prize_instance += 1

        prize_list_column.update()
        incorrect_answer(e)

    start = ft.Container(
        ft.CupertinoButton(
            content=ft.Text(
                "START THE CLOCK⏱️",
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
            on_click=start_timer,
        ),
        alignment=ft.alignment.center,
    )

    incorrect_button = ft.IconButton(
        icon=ft.icons.CLOSE_ROUNDED,
        icon_color=ft.colors.RED,
        on_click=incorrect_answer,
        icon_size=50,
    )

    correct_button = ft.IconButton(
        icon=ft.icons.CHECK_ROUNDED,
        icon_color=ft.colors.GREEN,
        on_click=correct_answer,
        icon_size=50,
    )

    bank = ft.IconButton(
        icon=ft.icons.MONEY,
        icon_color='#FF0098',
        on_click=prize_to_bank,
        icon_size=50,
    )

    # Button row
    button_row = ft.Row(
        [
            start
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Main UI layout
    main_content = ft.Row(
        [
            prizes_column,
            ft.Container(
                ft.Column(
                    [
                        countdown_column,
                        button_row,
                        ft.Divider(opacity=0),
                        ft.Divider(opacity=0),
                        ft.Divider(opacity=0),
                    ],
                    scroll=ft.ScrollMode.HIDDEN,
                    auto_scroll=False,
                    alignment=ft.MainAxisAlignment.CENTER,
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


ft.app(target=main, assets_dir='assets')
