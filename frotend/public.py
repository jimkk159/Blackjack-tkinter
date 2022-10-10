WHITE = "#DBDBDB"
blink_id = None


def toggle_color_fg(canvas, item, color_a, color_b):
    if type(item) == int:
        if canvas.itemcget(item, "fill") == color_a:
            canvas.itemconfig(item, fill=color_b)
        else:
            canvas.itemconfig(item, fill=color_a)
    else:
        if item.cget("fg") == color_a:
            item.config(fg=color_b)
        else:
            item.config(fg=color_a)


def toggle_color_bg(canvas, item, color_a, color_b):
    if type(item) == int:
        if canvas.itemcget(item, "fill") == color_a:
            canvas.itemconfig(item, fill=color_b)
        else:
            canvas.itemconfig(item, fill=color_a)
    else:
        if item.cget("bg") == color_a:
            item.config(bg=color_b)
        else:
            item.config(bg=color_a)


def start_blink(window, canvas, item, delay_time_bg, delay_time_fg, with_bg=False):
    global blink_id
    blink_id = None

    blink(window, canvas, item, delay_time_bg, delay_time_fg, with_bg)


def stop_blink(window):
    global blink_id

    if blink_id is not None:
        window.after_cancel(blink_id)


def blink(window, canvas, item, delay_time_bg, delay_time_fg, with_bg):
    global blink_id
    toggle_color_fg(canvas, item, "black", WHITE)

    if with_bg:
        toggle_color_bg(canvas, item, WHITE, "black")
    blink_id = window.after(delay_time_fg, blink, window, canvas, item, delay_time_fg, delay_time_bg, with_bg)
    # print(blink_id)

