# _*_ coding:utf-8 _*_
__author__ = "shisanjun"
import re

class AuditLogAnalysis(object):
    """
    对远程主机的strace日志文件进行分析，分析出执行命令
    """

    def __init__(self, logfile):
        self.logfile = logfile

    def parse(self):

        #用来存所有输入的命令
        cmd_output_list=[]
        #用来存所有输入的命令
        cmd_output_result=[]
        #输入的命令串
        output_str = ""

        #判断是不是要输出内容的标志
        input_flag = False

        # 左移右移计数，左移减1，右移加1
        move_left_right = 0

        #上下移动键
        move_up_down=0

        # 输出单个字段
        output_char = ""
        # 进入或者出vim标志
        input_vim=False
        #进入或者出vim编辑标志
        input_vim_flag = False
        output_vim_flag = False

        with open(self.logfile, 'r') as f:
            for line in f:
                if line:
                    sp = line.strip().split()
                    pid, time_clock, io_call, char = sp[0:4]
                    if str(io_call).startswith("read(5,"):
                        char = char.strip(',')

                        # 进入vim编辑模式
                        if char == '"\\33[>0;136;0c"':
                            cmd_output_result.append("进入vim编辑器")
                            input_vim_flag = True
                            input_vim=True

                        # 进入vim编辑模式
                        if input_vim_flag:
                            if char.strip('"') in ["i", "o", "A"]:
                                cmd_output_result.append("进入vim编辑模式")
                                input_vim_flag = False

                        # 退出编辑模式v
                        elif char == '"\\33"':
                            # 退出vim编辑器编辑模式,将前次输入内容输出来
                            cmd_output_result.append(output_str)
                            cmd_output_result.append("退出vim编辑模式")
                            output_str = ""
                            output_vim_flag = True
                            input_vim=False

                        # 鼠标上移
                        elif char == '"\\33[A"':
                            output_char = "[up 1]"

                        elif char == '"\\33[B"':  # 鼠标下移
                            output_char = "[down 1]"

                        # 鼠标右移
                        elif char == '"\\33[C"':
                            # print("鼠标右移动")
                            if abs(move_left_right) < len(output_str):
                                move_left_right += 1

                        # 鼠标左移
                        elif char == '"\\33[D"':
                            # print("鼠标左移动")
                            if abs(move_left_right) < len(output_str):
                                move_left_right -= 1

                        # 删除键del
                        elif char == '"\\33[3~"':
                            output_list = list(output_str)
                            output_list.pop(len(output_list) + move_left_right)
                            output_str = "".join(output_list)
                            # 删除一个，右移加1
                            move_left_right += 1

                        # 回退backspace
                        elif char == '"\\10"':
                            output_list = list(output_str)
                            if move_left_right == 0:
                                try:
                                    output_list.pop()
                                except:
                                    pass
                            else:
                                # 数组下标从0开始，所以需要多减个1
                                output_list.pop(len(output_list) + move_left_right - 1)
                            output_str = "".join(output_list)

                        elif char == '"\\n"':
                            output_char = ""

                        # 清空
                        elif char == '"\\7"':
                            output_str = ""

                        # 空格
                        elif char == '"':
                            output_char = ":"

                        # 回车换行
                        elif char == '"\\r"':
                            print(output_str)
                            #不是进入vim编辑模式
                            print(input_vim_flag)
                            if  not input_vim:

                                cmd_output_list.append(output_str)

                            # 退出vim编辑模式
                            if output_vim_flag:
                                if output_str in [":x", ":wq", ":q"]:
                                    cmd_output_result.append("退出vim编辑器")
                                    output_vim_flag = False
                            else:
                                cmd_output_result.append(output_str)
                            output_str = ""
                            move_left_right = 0
                        else:
                            output_char = char


                    # 判读是不是输入读取，后面跟有select(8:
                    if io_call == 'select(8,':
                        input_flag = True

                    # 有的read(5,后面是select(4 再select(8 去除这些数据
                    if io_call == 'select(4,':
                        output_char = ""

                    # 判断是不是正常输出
                    if input_flag:
                        # 输出字段不是空格式
                        if len(output_char) != 0:
                            insert_char = output_char.strip(',').strip('"').strip()
                        else:
                            insert_char = output_char

                        # 有没有移动左右键，没有移动过直接在后面追加
                        if move_left_right == 0:
                            output_str += insert_char
                        else:
                            output_list = list(output_str)
                            output_list.insert(len(output_list) + move_left_right, insert_char)
                            output_str = "".join(output_list)

                        output_char = ""
                        input_flag = False
        print(cmd_output_list,cmd_output_result)

if __name__ == "__main__":
    audit_obj = AuditLogAnalysis("20180314/session_31_8477a10c-30fa-4824-913b-87c5e34c0874.log")
    audit_obj.parse()
