from django.shortcuts import render
from forms import UploadFile
import re
import os
import pandas as pd
import time
from public_function import (all_fields, DOWNLOAD_DIR, DOWNLOAD_ROOT_DIR)

# Create your views here.


def parse_sdf(request):
    form = UploadFile()

    return render(request, 'index.html', {'form': form})


def result(request):
    if request.method == 'POST':
        form = UploadFile(request.POST, request.FILES)
        if form.is_valid():
            t = time.localtime()
            timestamp = time.strftime('%b-%d-%Y_%H%M', t)
            filename = 'result2.csv'
            relative_dir = os.path.join(DOWNLOAD_DIR, timestamp)
            relative_path = os.path.join(relative_dir, filename)
            full_dir = os.path.join(DOWNLOAD_ROOT_DIR, relative_dir)
            if not os.path.exists(full_dir):
                os.makedirs(full_dir)
            cd = form.cleaned_data
            if cd['file']:
                # data_file is the same as an opened file handle
                data_file = cd.get('file')
                a_line = ''
                total_recodes = []
                for i in data_file:
                    i = i.strip()
                    if i != '$$$$':
                        a_line += i + '@'
                    else:
                        total_recodes.append(a_line)
                        a_line = ''
                a_df = pd.DataFrame(columns=all_fields)
                count = 1
                for l in total_recodes:
                    line_value = []
                    # print(l)
                    for key in all_fields:
                        value = ''
                        if key == 'recode_id':
                            value = re.search(r'^(LMST\d+)', l).group(1)
                        else:
                            try:
                                value = re.search(r'{}>@(.*?)@'.format(key), l).group(1)
                            except:
                                print(key)
                        line_value.append(value)

                    a_df.loc[len(a_df)] = line_value
                a_df.to_csv(os.path.join(full_dir, filename), sep=',', index=False, header=True)
                count = len(a_df)
                return render(request, 'result.html', {'count': count, 'relative_path': relative_path})
            else:
                return render(request, 'There is something wrong.')

