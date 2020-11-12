import glob

science_goals = glob.glob("science_goal*")

all_flag_info = {}

for sg in science_goals:
    # walk only the science goals: walking other directories can be extremely
    # inefficient
    for dirpath, dirnames, filenames in os.walk(sg):
        if dirpath.count(os.path.sep) >= 5:
            # skip over things below the sci/gro/mou/<blah>/* level
            continue
        for fn in filenames:
            if (fn.endswith('12Mlong') or fn.endswith('12Mshort') or
                fn.endswith('7M') or fn.endswith('TP')):
                field_id = fn
        for fn in sorted(dirnames):
            if fn[-10:] == ".split.cal":

                fullfn = os.path.join(dirpath, fn)
                flagversions = flagmanager(fullfn, mode='list')

                all_flag_info[field_id] = {}

                for ii,fv in flagversions.items():
                    if 'name' in fv:
                        print(fv, fullfn)
                        flagmanager(fullfn, mode='restore', versionname=fv['name'])
                        flag_info = flagdata(vis=fullfn, mode='summary')
                        all_flag_info[field_id][fv['name']] = flag_info['field']

                        print(flag_info['field'], flag_info['field'][field_id]['flagged'] / flag_info['field'][field_id]['total'])



print({key: val['G353.41']['flagged'] / val['G353.41']['total'] for key, val in all_flag_info['G353.41_B3_12Mlong'].items()})
