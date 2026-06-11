import threading

from django.conf import settings


class MetricsMiddleware:
    _lock = threading.Lock()
    total = 0
    count_2xx = 0
    count_4xx = 0
    count_5xx = 0

    def __init__(self, get_response):
        self.get_response = get_response
        self.log_file = getattr(settings, "METRICS_LOG_FILE", None)

    def __call__(self, request):
        response = self.get_response(request)
        self._record(response.status_code)
        return response

    def _record(self, status_code):
        cls = type(self)
        with cls._lock:
            cls.total += 1
            if 200 <= status_code < 300:
                cls.count_2xx += 1
            elif 400 <= status_code < 500:
                cls.count_4xx += 1
            elif 500 <= status_code < 600:
                cls.count_5xx += 1
            line = (
                f"[METRICS] total={cls.total} "
                f"2xx={cls.count_2xx} 4xx={cls.count_4xx} 5xx={cls.count_5xx}"
            )

        print(line)
        if self.log_file:
            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(line + "\n")
            except OSError:
                pass
