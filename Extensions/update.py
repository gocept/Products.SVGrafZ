# explicit update

def update_all(self):
    ret = ''
    if self.meta_type == 'SVGrafZ':
        ret += "updating: %s\n" % '/'.join(self.getPhysicalPath())
        update = getattr(self, '_update')
        if callable(update):
            update()
    try:
        childs = self.objectValues()
    except AttributeError:
        childs = []
    for child in childs:
        ret += update_all(child)

    return ret
        

