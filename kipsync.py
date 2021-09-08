import pho2vis, sys

def args(string):
    if string == 'main':
        print('\n      pho2vis       Convert MIDI tracks of IPA phonemes to MIDI tracks of visemes compatible with OnyxToolkit')
        print('\n      help          Display details about a specific command\n')
    if string == 'help':
        print('\n      command       Command of interest\n')
    if string == 'pho2vis':
        print('\n      filename      Absolute or relative filepath to the target MIDI file')
        print('                    The phoneme tracks must be named as PHONEMES_GEORGE, PHONEMES_JOHN, and so on\n')

def dialog(string):
    strlist = string.split('_')
    if strlist[0] == 'inf':
        if strlist[1] == 'main':
            print('\nKipsync v' + version + ' by Kipnop')
        elif strlist[1] == 'help':
            print('\nhelp - Display details about a specific command')
        elif strlist[1] == 'pho2vis':
            print('\npho2vis - Convert MIDI tracks of IPA phonemes to MIDI tracks of visemes compatible with OnyxToolkit')
        args(strlist[1])
    elif strlist[0] == 'suc':
        if strlist[1] == 'pho2vis':
            print('\nSuccess: Created new midi file \'' + strlist[2] + '_KIPSYNC.mid\'\n')
    elif strlist[0] == 'err':
        if strlist[1] == 'missarg':
            print('\nError:   Missing required argument(s):')
            args(strlist[2])
        elif strlist[1] == 'cmdnf':
            print('\nError:   Command not found')
            args('main')
        elif strlist[1] == 'pho2vis':
            if strlist[2] == 'midnf':
                print('\nError:   MIDI file not found')
                dialog('inf_' + strlist[1])
            if strlist[2] == 'phonf':
                print('\nError:   Phoneme \'' + strlist[3] + '\' not found\n')
    sys.exit()

def main():
    global version
    version = '0.2.0-a'
    cmds = ['help', 'pho2vis']
    try:
        cmd = sys.argv[1]
    except IndexError:
        dialog('inf_main')
    if cmd == 'pho2vis':
        try:
            pho2vis.main(sys.argv[2])
        except IndexError:
            dialog('err_missarg_pho2vis')
    elif cmd == 'help':
        try:
            if sys.argv[2] in cmds:
                dialog('inf_' + sys.argv[2])
            else:
                dialog('err_cmdnf')
        except IndexError:
            dialog('inf_main')
    else:
        dialog('err_cmdnf')


if __name__ == '__main__':
    main()