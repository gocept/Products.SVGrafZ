# explicit update

def update_all(self):
    return _update_all_req(self) + "\nUpdate complete."

def _update_all_req(self):
    ret = ''
    if self.meta_type == 'SVGrafZ':
        ret += "updated: %s\n" % '/'.join(self.getPhysicalPath())
        update = getattr(self, '_update')
        if callable(update):
            update()
    try:
        childs = self.objectValues()
    except AttributeError:
        childs = []
    for child in childs:
        ret += _update_all_req(child)

    return ret
        

