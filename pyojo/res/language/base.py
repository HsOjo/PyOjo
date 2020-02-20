class Language:
    unknown = '? ? ?: (%s)'

    def __getattr__(self, key):
        if key not in dir(self):
            if '%s' in self.unknown:
                return self.unknown % key
            else:
                return self.unknown
