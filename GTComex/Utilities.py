def getValue(str_value):
    strval = str_value.strip().replace(',', '')
    return float(strval)


def convert2unicode(mydict):
    for k, v in mydict.iteritems():
        if isinstance(v, str):
            mydict[k] = unicode(v, errors='replace')
        elif isinstance(v, dict):
            convert2unicode(v)

