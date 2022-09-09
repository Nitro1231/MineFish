class Event:
    events = []
    count = 0

    def link(self, event) -> None:
        Event.events.append(event)

    def call(self) -> None:
        Event.count += 1
        print(f'called: {Event.count}')
        for e in Event.events:
            print(e)
            e()
