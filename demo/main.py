from app import App

if __name__ == "__main__":
    app = App()

    app.update()

    # app.launch_once()
    app.app_states['working_state'] = 0
    app.launch()

