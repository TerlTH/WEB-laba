import datetime

class ActionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Только логгируем действия, а не GET-запросы
        if request.method in ['POST', 'PUT', 'DELETE']:
            username = request.user.username if request.user.is_authenticated else 'Anonymous'
            path = request.path
            method = request.method
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            log_entry = f"[{now}] {username} → {method} {path}\n"

            with open("logs.txt", "a", encoding="utf-8") as log_file:
                log_file.write(log_entry)

        return response
