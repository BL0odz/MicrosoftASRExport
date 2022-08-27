# refs:
# https://github.com/commial/experiments/tree/master/windows-defender/ASR
# https://github.com/HansWessels/unluac
# https://github.com/hfiref0x/WDExtract

import os,sys,io
from subprocess import Popen
import parse

parsedLuacs = "luac_chunks/"
decompile_luas = "lua_decompiled/"

def start(VdmExtracted):
    f = open(VdmExtracted, 'rb')
    ll = f.read().split(b'\x1bLua')
    f.close()
    try:
        os.mkdir(parsedLuacs)
    except: pass
    print("\n\tnumber of chunks: " + str(len(ll)))
    for i in range(1, len(ll)):
        try:
            ans = parse.LuaFunc(io.BytesIO(b'\x1bLua' + ll[i])).export(root=True)
            open(parsedLuacs + "Luac_" + str(i), "wb").write(ans)
        except:
            print("\tSkip chunk : " + str(i))
    try:
        os.mkdir(decompile_luas)
    except: pass
    print("\n\tPlease wait for a few minutes...")
    for x in os.listdir(parsedLuacs):
        Popen("java.exe " + "-jar" + " unluac.jar " + parsedLuacs + x + ">" + decompile_luas + "MDASR_" + x + ".lua", shell=True)

if len(sys.argv) < 2:
    print("\n\tUsage: python MDASRLuaParse.py <VDM_filepth>")
else:
    os.system(os.getcwd() + "\\Bin\\bin64\\wdextract64.exe " + os.getcwd() + "\\" + sys.argv[1])
    start(sys.argv[1] + ".extracted")
