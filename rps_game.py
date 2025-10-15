import tkinter as tk
from tkinter import messagebox ,simpledialog
import random 
import datetime
import os 
import json

HISTORY_FILE ="rps_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE ,"r" ,encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return[]
    return[]

def save_history(history):
    try:
        with open(HISTORY_FILE,"w" ,encoding="utf-8")as f:
            json.dump(history ,f,ensure_ascii=False ,indent=2)
    except Exception as e :
        print("ERROR , saving history" , e)

OPTION = [" paper" ,"scissor" ," stone "]
WIN_PAIRS ={("paper","scissor") ,("paper" ,"stone"),("scissor" ,"stone")}

def decide(player , comp):
    if player == comp:
        return " Equal"
    return "win" if (player ,comp) in WIN_PAIRS else "Loss"
    
# ----- GUI -----
root =tk.Tk()
root.title("Paper | Stone | Scissor")
root.geometry("520x420")
root.resizable(False ,False)
root.configure(bg="#f4f7fb")

history =load_history()

# --Point Status --

player_score = 0
comp_score = 0


top_frame =tk.Frame(root ,bg="#f4f7fb")
top_frame.pack(pady=12 ,fill="x")

score_label = tk.Label(top_frame ,text=" Your point 0      :     Computer point 0" ,font=("Helvetica" ,14) ,bg="#f4f7fb")
score_label.pack()

choice_frame =tk.Frame(root, bg="#f4f7fb")
choice_frame.pack(pady=8)

player_choice_label =tk.Label(choice_frame ,text=" you :" ,font=("Helvetica" ,16) ,bg="#f4f7fb")
player_choice_label.grid(row=0 ,column=0 ,padx=20)
vs_label =tk.Label(choice_frame , text=" --" ,font=("Helvetica" ,16),bg="#f4f7fb")
vs_label.grid(row=0 ,column=1)
comp_choice_label =tk.Label(choice_frame , text="comp :--" ,font=("Helvetica" ,16) , bg="#f4f7fb")
comp_choice_label.grid(row=0 ,column=2 ,padx=20)

result_label =tk.Label(root , text=" " ,font=("Helvetica" ,18 ,"bold" ) , bg="#f4f7fb" ,fg="#333")
result_label.pack(pady=6)

button_frame =tk.Frame(root ,bg="#f4f7fb")
button_frame.pack(pady=6)

def play(player_choice):
    global player_score ,comp_score ,history
    comp =random.choice(OPTION)
    res= decide(player_choice ,comp)


    player_choice_label.config(text=f"You :{player_choice}")
    comp_choice_label.config(text=f"Computer : {comp}")


    if res == "win":
        player_score +=1
        result_label.config(text="You Win!" ,fg="#2e7d32")

    elif res=="Loss":
        comp_score +=1
        result_label.config(text="You Loss" ,fg="#c62828")

    else:
        result_label.config(text="Equal" ,fg="#023353")

    score_label.config(text=f"Your point : {player_score}  computer point :{comp_score}")

    entry ={"time" :
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,
            "player" :player_choice,
            "computer": comp,
            "result" :res}
    history.append(entry)
    save_history(history)  

#Buttons
btn_r =tk.Button(button_frame ,text="rock" ,width=12 ,height=2 ,font=("Hevetica" ,12) ,command =lambda:play("rock"))
btn_r.grid(row=0 ,column=0 ,padx=8 ,pady=6)

btn_p =tk.Button(button_frame ,text="paper" ,width=12 ,height=2 ,font=("Hevetica" ,12) ,command =lambda:play("paper"))
btn_p.grid(row=0 ,column=1 ,padx=8 ,pady=6)

btn_s =tk.Button(button_frame ,text="scissor" ,width=12 ,height=2 ,font=("Hevetica" ,12) ,command =lambda:play("scissor"))
btn_s.grid(row=0 ,column=2 ,padx=8 ,pady=6)


ctrl_frame =tk.Frame(root ,bg="#f4f7fb")
ctrl_frame.pack(pady=10 ,fill="x")

def reset_scors():
    global player_score ,comp_score
    if messagebox.askyesno("whether","you sure you want rest everything ?"):
        player_score =0
        comp_score =0
        score_label.config(text=f"_ your point :{player_score}  computer :{comp_score}")
        result_label.config(text=" ")

player_choice_label.config(text="you : _")
comp_choice_label.config(text="computer :  _")

def show_history_window():
    hist_win =tk.Toplevel(root)
    hist_win.title(" history game")
    hist_win.geometry("480x480")
    hist_win.config(bg="#ffffff")

    listbox =tk.Listbox(hist_win ,font=("Helvetica" ,11))
    listbox.pack(expand=True ,fill="both" ,padx=8 ,pady=8)

    for item in history:
        line = f"{item['time']} | you:{item['player']} | computer :{item['computer']} | => {item['result']}"
        listbox.insert(tk.END ,line)


    def clear_history():
        if messagebox.askyesno("clear history " ,"are you sure you want clear history?"):
            listbox.delete(0 ,tk.END)
            history.clear()
            save_history(history)


    tk.Button(hist_win , text="clear history" ,bg="#e57373" ,fg="white" ,command=clear_history).pack(pady=6)
    tk.Button(hist_win , text="close" ,command=hist_win.destroy).pack(pady=4)

def export_history(parent_window =None):
    path =simpledialog.askstring("enter name of output" ,"for example (my_history_txt)" )

    if not path:
        return
    try:
        with open(path ,"w" ,encoding="utf-8") as f:
            for item in history:
                f.write(f"{item['time']} | you {item['player']} | computer {item['computer']} => {item ['result']}\n")
                
        if parent_window:
            messagebox.showinfo("output saved" ,parent=parent_window)

            try:
                parent_window.destroy()
            except Exception:
                pass
        else:
            messagebox.showinfo("output saved")

    except Exception as e :
        if parent_window:
            messagebox.showerror("error" ,f"saving is not possible.:{e}" ,parent=parent_window)
        else:
            messagebox.showerror("error" ,f"saving is not possible.:{e}" )

tk.Button(ctrl_frame ,text="Point reset" ,bg="#64b5f6" ,command=reset_scors).pack(side="left" ,padx=22)
tk.Button(ctrl_frame ,text="History" ,bg="#81c784" ,command=show_history_window).pack(side="left" ,padx=22)
tk.Button(ctrl_frame ,text="Output" ,bg="#ffb74d" ,command=export_history).pack(side="left" ,padx=22)
tk.Button(ctrl_frame ,text="Exit" ,bg="#ef9a9a" ,command=root.quit).pack(side="right" ,padx=8) 
    


# SHORT GUIDE
footer =tk.Label(root ,text="Practice For More Points" ,bg="#ffb55d" ,fg="#555")
footer.pack(side="bottom" ,pady=6)


root.mainloop()