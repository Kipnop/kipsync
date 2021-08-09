import kipsync, mido, sys, yaml

def parse_msg(msg, curr_track):
    if msg.text[0] == '[':
        curr_track.append(mido.MetaMessage('text', text=msg.text, time=msg.time))
    elif msg.text.split('_')[0] == 'smile':
        curr_track.append(mido.MetaMessage('text', text='[l_smile_' + msg.text.split('_')[1] + ' ' + msg.text.split('_')[2] + ']', time=msg.time))
        curr_track.append(mido.MetaMessage('text', text='[r_smile_' + msg.text.split('_')[1] + ' ' + msg.text.split('_')[2] + ']', time=0))
    else:
        phoneme = msg.text.split('_')[0]
        try:
            curr_track.append(mido.MetaMessage('text', text=pvdict.get(phoneme)[0], time=msg.time))
        except TypeError:
            kipsync.dialog('err_pho2vis_phonf_' + phoneme)
        for vis in pvdict.get(phoneme)[1:]:
            if (('_' in msg.text) & ('jaw_open' in vis)):
                curr_track.append(mido.MetaMessage('text', text='[jaw_open ' + msg.text.split('_')[1] + ']', time=0))
            else:
                curr_track.append(mido.MetaMessage('text', text=vis, time=0))

def main(filename):
    try:
        mid = mido.MidiFile(filename)
    except FileNotFoundError:
        kipsync.dialog('err_pho2vis_midnf')
    global pvdict
    pvdict = yaml.load(open('pho2vis-dict.yml', 'r'), Loader=yaml.BaseLoader)
    for track in mid.tracks:
        if track.name in ['PHONEMES_GEORGE', 'PHONEMES_JOHN', 'PHONEMES_PAUL', 'PHONEMES_RINGO']:
            newtrack = mido.MidiTrack()
            newtrack.append(mido.MetaMessage('track_name', name='LIPSYNC_' + track.name[9:]))
            for msg in track:
                if msg.type == 'text':
                    parse_msg(msg, newtrack)
            mid.tracks.append(newtrack)
    mid.save(filename[:-4] + '_KIPSYNC.mid')
    kipsync.dialog('suc_pho2vis_' + filename[:-4])

if __name__ == '__main__':
    main(sys.argv[1])