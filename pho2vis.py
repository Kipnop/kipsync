import kipsync, mido, sys, yaml

def parse_msg(msg, curr_track, dict, timeacc):
    if msg.text[0] == '[':
        curr_track.append(mido.MetaMessage('text', text=msg.text, time=msg.time + timeacc))
        return 0
    elif msg.text.split(' ')[0] == 'smile':
        curr_track.append(mido.MetaMessage('text', text='[l_smile_' + msg.text.split(' ')[1] + ' ' + msg.text.split('_')[2] + ']', time=msg.time + timeacc))
        curr_track.append(mido.MetaMessage('text', text='[r_smile_' + msg.text.split(' ')[1] + ' ' + msg.text.split('_')[2] + ']', time=0))
        return 0
    elif msg.text.split(' ')[0] == 'happy':
        happy = msg.text.split(' ')[1]
        return msg.time + timeacc
    elif msg.text.split(' ')[0] == 'brows_inner':
        browval = msg.text.split(' ')[1]
        val1 = max(0, browval)
        val2 = 0 - min(0, browval)
        curr_track.append(mido.MetaMessage('text', text='[m_brow_up ' + val1 + ']', time=msg.time + timeacc))
        curr_track.append(mido.MetaMessage('text', text='[m_brow_dn ' + val2 + ']', time=0))
        return 0
    elif msg.text.split(' ')[0] == 'brows_outer':
        browval = msg.text.split(' ')[1]
        val1 = max(0, browval)
        val2 = 0 - min(0, browval)
        curr_track.append(mido.MetaMessage('text', text='[l_brow_up ' + val1 + ']', time=msg.time + timeacc))
        curr_track.append(mido.MetaMessage('text', text='[l_brow_dn ' + val2 + ']', time=0))
        curr_track.append(mido.MetaMessage('text', text='[r_brow_up ' + val1 + ']', time=0))
        curr_track.append(mido.MetaMessage('text', text='[r_brow_dn ' + val2 + ']', time=0))
        return 0
    elif msg.text.split(' ')[0] == 'lids':
        lidsval = msg.text.split(' ')[1]
        curr_track.append(mido.MetaMessage('text', text='[l_lids ' + lidsval + ']', time=msg.time + timeacc))
        curr_track.append(mido.MetaMessage('text', text='[r_lids ' + lidsval + ']', time=0))
        return 0
    elif msg.text.split(' ')[0] == 'squint':
        squintval = msg.text.split(' ')[1]
        curr_track.append(mido.MetaMessage('text', text='[l_squint ' + squintval + ']', time=msg.time + timeacc))
        curr_track.append(mido.MetaMessage('text', text='[r_squint ' + squintval + ']', time=0))
        return 0
    else:
        phoneme = msg.text.split(' ')[0]
        try:
            curr_track.append(mido.MetaMessage('text', text=dict.get(phoneme)[0], time=msg.time + timeacc))
        except TypeError:
            kipsync.dialog('err_pho2vis_phonf_' + phoneme)
        for vis in dict.get(phoneme)[1:]:
            if ((' ' in msg.text) & ('jaw_open' in vis)):
                curr_track.append(mido.MetaMessage('text', text='[jaw_open ' + msg.text.split(' ')[1] + ']', time=0))
            else:
                curr_track.append(mido.MetaMessage('text', text=vis, time=0))
        return 0

def main(filename):
    try:
        mid = mido.MidiFile(filename)
    except FileNotFoundError:
        kipsync.dialog('err_pho2vis_midnf')
    global happy, timeacc
    for track in mid.tracks:
        if track.name in ['PHONEMES_GEORGE', 'PHONEMES_JOHN', 'PHONEMES_PAUL', 'PHONEMES_RINGO']:
            beatle = track.name[9:].lower()
            pvdict = yaml.load(open('pho2vis-dict-' + beatle + '.yml', 'r'), Loader=yaml.BaseLoader)
            newtrack = mido.MidiTrack()
            newtrack.append(mido.MetaMessage('track_name', name='LIPSYNC_' + track.name[9:]))
            happy = 0
            timeacc = 0
            for msg in track:
                if msg.type == 'text':
                    timeacc = parse_msg(msg, newtrack, pvdict, timeacc)
            mid.tracks.append(newtrack)
    mid.save(filename[:-4] + '_KIPSYNC.mid')
    kipsync.dialog('suc_pho2vis_' + filename[:-4])

if __name__ == '__main__':
    main(sys.argv[1])