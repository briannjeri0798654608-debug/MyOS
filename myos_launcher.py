
import tkinter as tk
from tkinter import messagebox, simpledialog
import json, os, datetime, time, hashlib, subprocess

BASE = os.path.expanduser("~/.myos")
FS_FILE = BASE + "/filesystem.json"
USER_FILE = BASE + "/users.json"
os.makedirs(BASE, exist_ok=True)

BG="#0a0a0f"; BG2="#12121a"; BG3="#1a1a2e"
ACCENT="#00d4ff"; ACCENT2="#7b2fff"; GREEN="#00ff88"
RED="#ff4444"; YELLOW="#ffd700"; WHITE="#ffffff"
GRAY="#888888"; TASKBAR="#0d0d1a"
FSM=("Monospace",11); FMD=("Monospace",14,"bold"); FTL=("Monospace",18,"bold")

def lj(p,d):
    if os.path.exists(p):
        with open(p) as f: return json.load(f)
    return d

def sj(p,data):
    with open(p,"w") as f: json.dump(data,f)

def hp(pw): return hashlib.sha256(pw.encode()).hexdigest()

class Login(tk.Frame):
    def __init__(self,master,cb):
        super().__init__(master,bg=BG)
        self.master=master; self.cb=cb
        self.users=lj(USER_FILE,{})
        self.pack(fill="both",expand=True)
        tk.Label(self,text="",bg=BG).pack(expand=True)
        tk.Label(self,text="⬡",font=("Monospace",60),fg=ACCENT,bg=BG).pack()
        tk.Label(self,text="MyOS",font=("Monospace",36,"bold"),fg=WHITE,bg=BG).pack()
        tk.Label(self,text="v2.0 Graphical",font=FSM,fg=ACCENT,bg=BG).pack()
        tk.Label(self,text="",bg=BG).pack(pady=10)
        box=tk.Frame(self,bg=BG3,padx=30,pady=30)
        box.pack(padx=60,pady=10,fill="x")
        tk.Label(box,text="Username",font=FSM,fg=GRAY,bg=BG3).pack(anchor="w")
        self.ue=tk.Entry(box,font=FMD,bg=BG2,fg=WHITE,insertbackground=ACCENT,relief="flat",bd=5)
        self.ue.pack(fill="x",pady=(2,10)); self.ue.focus()
        tk.Label(box,text="Password",font=FSM,fg=GRAY,bg=BG3).pack(anchor="w")
        self.pe=tk.Entry(box,font=FMD,bg=BG2,fg=WHITE,insertbackground=ACCENT,relief="flat",bd=5,show="*")
        self.pe.pack(fill="x",pady=(2,10))
        self.pe.bind("<Return>",lambda e:self.login())
        self.msg=tk.Label(box,text="",font=FSM,fg=RED,bg=BG3)
        self.msg.pack()
        bf=tk.Frame(box,bg=BG3); bf.pack(fill="x",pady=5)
        tk.Button(bf,text="LOGIN",font=FMD,bg=ACCENT,fg=BG,relief="flat",pady=8,cursor="hand2",command=self.login).pack(side="left",expand=True,fill="x",padx=(0,5))
        tk.Button(bf,text="NEW USER",font=FMD,bg=ACCENT2,fg=WHITE,relief="flat",pady=8,cursor="hand2",command=self.register).pack(side="left",expand=True,fill="x")
        tk.Label(self,text="",bg=BG).pack(expand=True)
        self.clk=tk.Label(self,text="",font=FMD,fg=ACCENT,bg=BG)
        self.clk.pack(pady=5); self.tick()
    def tick(self):
        self.clk.config(text=datetime.datetime.now().strftime("%H:%M:%S  |  %A %d %B %Y"))
        self.after(1000,self.tick)
    def login(self):
        u=self.ue.get().strip(); p=self.pe.get()
        if not u or not p: self.msg.config(text="Fill all fields"); return
        if u not in self.users: self.msg.config(text="User not found"); return
        if self.users[u]["password"]!=hp(p): self.msg.config(text="Wrong password"); return
        self.destroy(); self.cb(u)
    def register(self):
        u=simpledialog.askstring("New User","Username:",parent=self)
        if not u: return
        if u in self.users: messagebox.showerror("Error","Exists"); return
        p=simpledialog.askstring("Password","Password:",show="*",parent=self)
        if not p: return
        self.users[u]={"password":hp(p),"created":str(datetime.datetime.now())[:19]}
        sj(USER_FILE,self.users)
        messagebox.showinfo("Done",f"Account created: {u}")
        self.ue.delete(0,"end"); self.ue.insert(0,u)

class Desktop(tk.Frame):
    def __init__(self,master,user):
        super().__init__(master,bg=BG)
        self.master=master; self.user=user
        self.fs=lj(FS_FILE,{}); self.t0=time.time()
        self.pack(fill="both",expand=True)
        self.cv=tk.Canvas(self,bg=BG,highlightthickness=0)
        self.cv.pack(fill="both",expand=True)
        self.wallpaper()
        self.icons()
        tb=tk.Frame(self,bg=TASKBAR,height=55)
        tb.pack(fill="x",side="bottom"); tb.pack_propagate(False)
        tk.Button(tb,text=" ⬡ MyOS ",font=FSM,bg=ACCENT,fg=BG,relief="flat",cursor="hand2",command=self.menu).pack(side="left",padx=5,pady=8)
        tk.Label(tb,text=f"👤 {user}",font=FSM,fg=GREEN,bg=TASKBAR).pack(side="right",padx=10)
        self.clk=tk.Label(tb,text="",font=FSM,fg=ACCENT,bg=TASKBAR)
        self.clk.pack(side="right",padx=10); self.tick()
    def tick(self):
        self.clk.config(text=datetime.datetime.now().strftime("%H:%M"))
        self.after(1000,self.tick)
    def wallpaper(self):
        c=self.cv
        c.create_rectangle(0,0,1080,1920,fill="#050510",outline="")
        for i in range(6):
            v=10+i*15; col=f"#{v:02x}{v:02x}{v+20:02x}"
            c.create_oval(-50+i*80,-50+i*80,1130-i*80,1970-i*80,fill=col,outline="")
        for x,y,r,col in [(150,300,160,"#00d4ff"),(900,600,200,"#7b2fff"),(300,1300,140,"#00ff88"),(800,1500,120,"#ff4444")]:
            for i in range(5,0,-1):
                c.create_oval(x-r*i//5,y-r*i//5,x+r*i//5,y+r*i//5,fill="",outline=col,width=i)
        c.create_text(540,960,text="MyOS",font=("Monospace",90,"bold"),fill="#ffffff")
    def icons(self):
        apps=[("🖥️","Terminal",self.term,80,160),("📁","Files",self.files,80,340),("📊","Tasks",self.tasks,80,520),("🧮","Calc",self.calc,80,700),("📝","Notes",self.notes,80,880),("ℹ️","System",self.sysinfo,80,1060),("🌐","Browser",self.browser,980,160),("🎵","Music",self.music,980,340),("⚙️","Settings",self.settings,980,520)]
        for em,nm,fn,x,y in apps:
            self.cv.create_rectangle(x-50,y-50,x+50,y+50,fill=BG3,outline=ACCENT,width=2,tags=nm)
            self.cv.create_text(x,y-12,text=em,font=("Monospace",28),tags=nm)
            self.cv.create_text(x,y+32,text=nm,font=("Monospace",10),fill=WHITE,tags=nm)
            self.cv.tag_bind(nm,"<Button-1>",lambda e,f=fn:f())
            self.cv.tag_bind(nm,"<Enter>",lambda e,n=nm:self.cv.itemconfig(n,fill=ACCENT2))
            self.cv.tag_bind(nm,"<Leave>",lambda e,n=nm:self.cv.itemconfig(n,fill=BG3))
    def menu(self):
        m=tk.Menu(self,tearoff=0,bg=BG3,fg=WHITE,activebackground=ACCENT,activeforeground=BG,font=FSM)
        for lbl,fn in [("🖥️  Terminal",self.term),("📁  Files",self.files),("📊  Task Manager",self.tasks),("🧮  Calculator",self.calc),("📝  Notes",self.notes),("ℹ️   System",self.sysinfo),("🌐  Browser",self.browser),("🎵  Music",self.music),("⚙️  Settings",self.settings)]:
            m.add_command(label=lbl,command=fn)
        m.add_separator()
        m.add_command(label="🔒  Logout",command=self.logout)
        m.add_command(label="⏻   Shutdown",command=self.shutdown)
        m.post(5,self.winfo_height()-60)
    def win(self,title,w=520,h=440):
        W=tk.Toplevel(self,bg=BG2); W.title(title); W.geometry(f"{w}x{h}+100+100")
        bar=tk.Frame(W,bg=BG3,height=36); bar.pack(fill="x"); bar.pack_propagate(False)
        tk.Label(bar,text=title,font=FSM,fg=ACCENT,bg=BG3).pack(side="left",padx=10)
        tk.Button(bar,text="✕",fg=RED,bg=BG3,relief="flat",cursor="hand2",command=W.destroy).pack(side="right",padx=5)
        return W
    def term(self):
        W=self.win("🖥️ Terminal",600,500)
        out=tk.Text(W,bg="#000",fg=GREEN,font=("Monospace",11),insertbackground=GREEN,relief="flat",padx=8)
        out.pack(fill="both",expand=True)
        fs=self.fs; t0=time.time()
        def wr(t): out.insert("end",t); out.see("end")
        def run(e=None):
            cmd=en.get().strip(); en.delete(0,"end")
            if not cmd: return
            wr(f"\n{self.user}@myos> {cmd}\n")
            p=cmd.split(None,3); c=p[0]; a1=p[1] if len(p)>1 else ""
            if c=="help": wr("  ls  write <f> <d>  read <f>  del <f>\n  meminfo  calc <n><op><n>  date  uptime  clear\n")
            elif c=="ls":
                if fs:
                    for n,v in fs.items(): wr(f"  📄 {n}  {len(v['data'])}b  [{v.get('owner','?')}]\n")
                else: wr("  (empty)\n")
            elif c=="write":
                d=" ".join(p[2:]); fs[a1]={"data":d,"owner":self.user,"modified":str(datetime.datetime.now())[:19]}; sj(FS_FILE,fs); wr(f"  ✓ {a1} saved\n")
            elif c=="read": wr(f"  {fs[a1]['data']}\n" if a1 in fs else "  Not found\n")
            elif c=="del":
                if a1 in fs: del fs[a1]; sj(FS_FILE,fs); wr("  ✓ Deleted\n")
            elif c=="meminfo": u=sum(len(v["data"]) for v in fs.values()); wr(f"  Total:65536 Used:{u} Free:{65536-u}\n")
            elif c=="calc":
                try: pp=cmd.split(); wr(f"  = {eval(pp[1]+pp[2]+pp[3])}\n")
                except: wr("  Error\n")
            elif c=="date": wr(f"  {datetime.datetime.now()}\n")
            elif c=="uptime": s=int(time.time()-t0); wr(f"  {s//3600}h {(s%3600)//60}m {s%60}s\n")
            elif c=="clear": out.delete("1.0","end")
            else: wr(f"  Unknown: {c}\n")
        wr(f"MyOS Terminal | {self.user}@myos\nhelp for commands\n\n{self.user}@myos> ")
        en=tk.Entry(W,font=("Monospace",12),bg="#000",fg=GREEN,insertbackground=GREEN,relief="flat")
        en.pack(fill="x",padx=5,pady=5); en.bind("<Return>",run); en.focus()
    def files(self):
        W=self.win("📁 Files",550,450); fs=self.fs
        def ref():
            for w in lf.winfo_children(): w.destroy()
            if not fs: tk.Label(lf,text="No files",font=FSM,fg=GRAY,bg=BG2).pack(pady=20); return
            tk.Label(lf,text=f"  {'Name':<25}{'Size':>8}  Owner",font=("Monospace",10),fg=ACCENT,bg=BG3).pack(fill="x")
            for n,v in fs.items():
                r=tk.Frame(lf,bg=BG2); r.pack(fill="x",pady=1)
                tk.Label(r,text=f"  📄 {n:<24}{len(v['data']):>7}b  {v.get('owner','?')}",font=("Monospace",10),fg=WHITE,bg=BG2,anchor="w").pack(side="left",fill="x",expand=True)
                tk.Button(r,text="✕",fg=RED,bg=BG2,relief="flat",cursor="hand2",command=lambda n=n:dlf(n)).pack(side="right")
        def dlf(n):
            if messagebox.askyesno("Delete",f"Delete {n}?"): del fs[n]; sj(FS_FILE,fs); ref()
        def nwf():
            n=simpledialog.askstring("New","Name:",parent=W)
            if not n: return
            d=simpledialog.askstring("Content","Data:",parent=W) or ""
            fs[n]={"data":d,"owner":self.user,"modified":str(datetime.datetime.now())[:19]}; sj(FS_FILE,fs); ref()
        tb=tk.Frame(W,bg=BG3); tb.pack(fill="x",padx=5,pady=5)
        tk.Button(tb,text="+ New",font=FSM,bg=GREEN,fg=BG,relief="flat",cursor="hand2",command=nwf).pack(side="left",padx=5)
        tk.Button(tb,text="↻",font=FSM,bg=ACCENT,fg=BG,relief="flat",cursor="hand2",command=ref).pack(side="left")
        lf=tk.Frame(W,bg=BG2); lf.pack(fill="both",expand=True,padx=5); ref()
    def tasks(self):
        W=self.win("📊 Task Manager",560,500)
        def ref():
            for w in cf.winfo_children(): w.destroy()
            try:
                with open("/proc/stat") as f: s=f.readline().split()
                v=[int(x) for x in s[1:]]; time.sleep(0.15)
                with open("/proc/stat") as f: s=f.readline().split()
                v2=[int(x) for x in s[1:]]; dt=sum(v2)-sum(v); di=v2[3]-v[3]
                cpu=round(100*(dt-di)/dt,1) if dt else 0
            except: cpu=0
            try:
                mi={}
                with open("/proc/meminfo") as f:
                    for l in f:
                        pp=l.split()
                        if len(pp)>=2: mi[pp[0].rstrip(":")]=int(pp[1])
                tot=mi.get("MemTotal",0); av=mi.get("MemAvailable",0); us=tot-av; pct=int(us/tot*100) if tot else 0
            except: tot=us=pct=0
            cc=GREEN if cpu<50 else YELLOW if cpu<80 else RED
            mc=GREEN if pct<50 else YELLOW if pct<80 else RED
            tk.Label(cf,text=f"CPU: {cpu}%",font=FTL,fg=cc,bg=BG2).pack(pady=4)
            cb=tk.Canvas(cf,height=22,bg=BG3,highlightthickness=0); cb.pack(fill="x",padx=20); cb.update()
            cb.create_rectangle(0,0,int(cb.winfo_width()*cpu/100),22,fill=cc,outline="")
            tk.Label(cf,text=f"RAM: {us//1024}MB / {tot//1024}MB ({pct}%)",font=FTL,fg=mc,bg=BG2).pack(pady=4)
            mb=tk.Canvas(cf,height=22,bg=BG3,highlightthickness=0); mb.pack(fill="x",padx=20); mb.update()
            mb.create_rectangle(0,0,int(mb.winfo_width()*pct/100),22,fill=mc,outline="")
            tk.Label(cf,text=f"  {'PID':<8}{'CPU%':<8}{'MEM%':<8}Process",font=("Monospace",10),fg=ACCENT,bg=BG3).pack(fill="x",pady=4)
            try:
                r=subprocess.run(["ps","-eo","pid,pcpu,pmem,comm"],capture_output=True,text=True)
                for line in r.stdout.strip().split("\n")[1:15]:
                    pp=line.split(None,3)
                    if len(pp)==4: tk.Label(cf,text=f"  {pp[0]:<8}{pp[1]:<8}{pp[2]:<8}{pp[3][:22]}",font=("Monospace",10),fg=WHITE,bg=BG2,anchor="w").pack(fill="x")
            except: pass
        tk.Button(W,text="↻ Refresh",font=FSM,bg=ACCENT,fg=BG,relief="flat",cursor="hand2",command=ref).pack(pady=5)
        cf=tk.Frame(W,bg=BG2); cf.pack(fill="both",expand=True,padx=5); ref()
    def calc(self):
        W=self.win("🧮 Calculator",320,460)
        ex=tk.StringVar(value="0")
        tk.Label(W,textvariable=ex,font=("Monospace",28,"bold"),fg=WHITE,bg="#000",anchor="e",padx=10).pack(fill="x",pady=10,padx=10)
        def pr(v):
            cur=ex.get()
            if v=="C": ex.set("0")
            elif v=="=":
                try: ex.set(str(eval(cur.replace("×","*").replace("÷","/"))))
                except: ex.set("Err")
            elif v=="⌫": ex.set(cur[:-1] if len(cur)>1 else "0")
            else: ex.set(("" if cur=="0" else cur)+str(v))
        for row in [["C","⌫","%","÷"],["7","8","9","×"],["4","5","6","-"],["1","2","3","+"],[" ","0",".","="]]:
            rf=tk.Frame(W,bg=BG2); rf.pack(fill="x",padx=10,pady=2)
            for b in row:
                if b==" ": tk.Label(rf,text="",bg=BG2,width=5).pack(side="left",expand=True,fill="x",padx=2); continue
                col={"C":RED,"⌫":YELLOW,"=":GREEN,"÷":ACCENT,"×":ACCENT,"-":ACCENT,"+":ACCENT,"%":ACCENT}.get(b,BG3)
                fg2=BG if col in [GREEN,RED,YELLOW] else WHITE
                tk.Button(rf,text=b,font=FMD,bg=col,fg=fg2,relief="flat",width=4,pady=12,cursor="hand2",command=lambda v=b:pr(v)).pack(side="left",expand=True,fill="x",padx=2)
    def notes(self):
        W=self.win("📝 Notes",520,500); fs=self.fs
        lb=tk.Listbox(W,bg=BG3,fg=WHITE,font=FSM,selectbackground=ACCENT,selectforeground=BG,relief="flat",width=18)
        lb.pack(side="left",fill="y",padx=5,pady=5)
        ta=tk.Text(W,bg="#000",fg=GREEN,font=("Monospace",12),insertbackground=GREEN,relief="flat",padx=8)
        ta.pack(side="left",fill="both",expand=True,padx=5,pady=5)
        def load():
            lb.delete(0,"end")
            for n in fs: lb.insert("end",n)
        def sel(e):
            s=lb.curselection()
            if s: ta.delete("1.0","end"); ta.insert("1.0",fs[lb.get(s[0])]["data"])
        def save():
            n=simpledialog.askstring("Save","Filename:",parent=W)
            if not n: return
            d=ta.get("1.0","end").strip()
            fs[n]={"data":d,"owner":self.user,"modified":str(datetime.datetime.now())[:19]}; sj(FS_FILE,fs); load()
        lb.bind("<<ListboxSelect>>",sel)
        tk.Button(W,text="💾 Save",font=FSM,bg=GREEN,fg=BG,relief="flat",cursor="hand2",command=save).pack(side="bottom",pady=5)
        load()
    def sysinfo(self):
        W=self.win("ℹ️ System",440,400)
        try:
            mi={}
            with open("/proc/meminfo") as f:
                for l in f:
                    pp=l.split()
                    if len(pp)>=2: mi[pp[0].rstrip(":")]=int(pp[1])
            tot=mi.get("MemTotal",0); av=mi.get("MemAvailable",0)
        except: tot=av=0
        s=int(time.time()-self.t0)
        for k,v in [("OS","MyOS v2.0 GUI"),("User",self.user),("Arch","ARM64 Redmi 14C"),("RAM Total",f"{tot//1024} MB"),("RAM Free",f"{av//1024} MB"),("Files",f"{len(self.fs)}/16"),("Uptime",f"{s//3600}h {(s%3600)//60}m {s%60}s"),("Date",str(datetime.datetime.now())[:19]),("Display","VNC :1")]:
            r=tk.Frame(W,bg=BG2); r.pack(fill="x",padx=20,pady=4)
            tk.Label(r,text=f"{k}:",font=FSM,fg=ACCENT,bg=BG2,width=14,anchor="w").pack(side="left")
            tk.Label(r,text=v,font=FSM,fg=WHITE,bg=BG2).pack(side="left")
    def browser(self):
        W=self.win("🌐 MyOS Browser",600,520)
        tk.Label(W,text="MyOS Browser",font=FTL,fg=ACCENT,bg=BG2).pack(pady=10)
        bar=tk.Frame(W,bg=BG3); bar.pack(fill="x",padx=10,pady=5)
        url=tk.Entry(bar,font=FSM,bg=BG2,fg=WHITE,insertbackground=ACCENT,relief="flat",bd=5)
        url.pack(side="left",fill="x",expand=True,padx=5)
        url.insert(0,"https://")
        content=tk.Text(W,bg="#000",fg=GREEN,font=("Monospace",10),relief="flat",padx=10,pady=10)
        content.pack(fill="both",expand=True,padx=10,pady=5)
        def go():
            u=url.get().strip()
            content.delete("1.0","end")
            content.insert("end",f"Loading: {u}\n\n")
            try:
                import urllib.request
                req=urllib.request.Request(u,headers={"User-Agent":"MyOSBrowser/2.0"})
                with urllib.request.urlopen(req,timeout=8) as r:
                    raw=r.read(8000).decode("utf-8","ignore")
                import re
                txt=re.sub(r"<[^>]+>","",raw)
                txt=re.sub(r"\s+"," ",txt).strip()
                content.insert("end",txt[:3000])
            except Exception as e:
                content.insert("end",f"Error: {e}\n\nNote: VNC has limited internet access.\nTry: http://example.com")
        tk.Button(bar,text="Go",font=FSM,bg=ACCENT,fg=BG,relief="flat",cursor="hand2",command=go).pack(side="left",padx=5)
        url.bind("<Return>",lambda e:go())
        favs=["https://example.com","https://google.com","https://wikipedia.org"]
        ff=tk.Frame(W,bg=BG3); ff.pack(fill="x",padx=10,pady=2)
        tk.Label(ff,text="Bookmarks:",font=FSM,fg=GRAY,bg=BG3).pack(side="left",padx=5)
        for f in favs:
            tk.Button(ff,text=f.replace("https://","").replace("http://","")[:15],font=("Monospace",9),bg=BG2,fg=ACCENT,relief="flat",cursor="hand2",command=lambda u=f:(url.delete(0,"end"),url.insert(0,u),go())).pack(side="left",padx=2)
    def music(self):
        W=self.win("🎵 Music Player",400,500)
        tk.Label(W,text="🎵",font=("Monospace",60),bg=BG2).pack(pady=10)
        self.song_var=tk.StringVar(value="No song loaded")
        tk.Label(W,textvariable=self.song_var,font=FSM,fg=WHITE,bg=BG2,wraplength=360).pack(pady=5)
        import glob
        songs=glob.glob(os.path.expanduser("~/Music/*.mp3"))+glob.glob(os.path.expanduser("~/storage/music/*.mp3"))+glob.glob("/sdcard/Music/*.mp3")
        lb=tk.Listbox(W,bg=BG3,fg=WHITE,font=("Monospace",10),selectbackground=ACCENT,relief="flat",height=8)
        lb.pack(fill="both",expand=True,padx=10,pady=5)
        if songs:
            for s in songs: lb.insert("end",os.path.basename(s))
        else:
            lb.insert("end","No MP3 files found")
            lb.insert("end","Put MP3s in ~/Music/")
        self.player_proc=None
        def play():
            sel=lb.curselection()
            if not sel or not songs: return
            song=songs[sel[0]]
            self.song_var.set(f"▶ {os.path.basename(song)}")
            if self.player_proc: self.player_proc.terminate()
            self.player_proc=subprocess.Popen(["mpv","--no-video",song],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        def stop():
            if self.player_proc: self.player_proc.terminate()
            self.song_var.set("⏹ Stopped")
        ctrl=tk.Frame(W,bg=BG2); ctrl.pack(pady=10)
        tk.Button(ctrl,text="▶ Play",font=FMD,bg=GREEN,fg=BG,relief="flat",padx=15,pady=8,cursor="hand2",command=play).pack(side="left",padx=5)
        tk.Button(ctrl,text="⏹ Stop",font=FMD,bg=RED,fg=WHITE,relief="flat",padx=15,pady=8,cursor="hand2",command=stop).pack(side="left",padx=5)
        tk.Label(W,text="Install mpv: pkg install mpv",font=("Monospace",9),fg=GRAY,bg=BG2).pack(pady=5)
    def settings(self):
        W=self.win("⚙️ Settings",460,520)
        tk.Label(W,text="⚙️ MyOS Settings",font=FTL,fg=ACCENT,bg=BG2).pack(pady=15)
        cfg_file=os.path.expanduser("~/.myos/config.json")
        cfg=lj(cfg_file,{})
        sections=[
            ("👤 Account",""),
            ("Username",self.user),
            ("Created",lj(USER_FILE,{}).get(self.user,{}).get("created","?")),
            ("💾 Storage",""),
            ("Files saved",str(len(self.fs))+"/16"),
            ("Storage path","~/.myos/"),
            ("🖥️ Display",""),
            ("Resolution","1080x1920"),
            ("VNC Port","5901"),
            ("Theme","Dark Neon"),
            ("⚡ System",""),
            ("Python","3.13"),
            ("Arch","ARM64"),
            ("Device","Redmi 14C"),
        ]
        for k,v in sections:
            if not v:
                tk.Label(W,text=k,font=FMD,fg=ACCENT2,bg=BG3).pack(fill="x",padx=15,pady=(10,2))
            else:
                r=tk.Frame(W,bg=BG2); r.pack(fill="x",padx=20,pady=2)
                tk.Label(r,text=f"{k}:",font=FSM,fg=GRAY,bg=BG2,width=16,anchor="w").pack(side="left")
                tk.Label(r,text=v,font=FSM,fg=WHITE,bg=BG2,anchor="w").pack(side="left")
        tk.Button(W,text="🔒 Change Password",font=FSM,bg=ACCENT2,fg=WHITE,relief="flat",pady=6,cursor="hand2",command=lambda:self.chpw(W)).pack(pady=15,padx=20,fill="x")
    def chpw(self,parent):
        p=simpledialog.askstring("Password","New password:",show="*",parent=parent)
        if not p: return
        users=lj(USER_FILE,{})
        users[self.user]["password"]=hp(p)
        sj(USER_FILE,users)
        messagebox.showinfo("Done","Password changed!")
    def logout(self):
        if messagebox.askyesno("Logout","Return to login?"): self.destroy(); Login(self.master,lambda u:Desktop(self.master,u))
    def shutdown(self):
        if messagebox.askyesno("Shutdown","Shutdown MyOS?"): self.master.quit()

import os as _os, json as _json
_cfg = _os.path.expanduser('~/.myos/config.json')
_auto = None
if _os.path.exists(_cfg):
    with open(_cfg) as _f: _auto = _json.load(_f).get('autologin')
root=tk.Tk()
root.title("MyOS v2.0")
root.geometry("1080x1920")
root.configure(bg=BG)
if _auto:
    Desktop(root, _auto)
else:
    Login(root,lambda u:Desktop(root,u))
root.mainloop()
