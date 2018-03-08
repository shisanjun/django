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

        output_str = ""
        # vim_flag代表是否使用了vim工具
        vim_flag = False
        input_flag = False
        output_len=0
        right_count=0
        left_count=0
        with open(self.logfile, 'r') as f:
            for line in f:
                if line:
                    sp = line.strip().split()
                    pid, time_clock, io_call, char = sp[0:4]
                    # #vim 模式分析
                    if str(io_call).startswith("read(5,"):

                        char=char.strip(',').strip('"').strip()
                        #print(char)
                        # 进入vim编辑模式
                        if char == '"\33[>0;136;0c",':
                            input_char = "进入编辑模式"
                            vim_flag = True

                        if vim_flag:  # 在vim编辑模式下
                            if char == '"\\33OA",':  # 鼠标上移
                                input_char = "[up 1]"
                            if char == '"\\33OB",':  # 鼠标下移
                                input_char = "[down 1]"
                            if char == '"\\33OC",':  # 鼠标右移
                                input_char = "[right 1]"


                            if char == '"\\33OD",':  # 鼠标左移
                                input_char = "[left 1]"
                            if char == '"\\r",':  # 回车换行
                                input_char = "回车换行"
                            output_str += input_char

                            if char == "\\33":
                                char = "退出编辑模式"
                                print(output_str)
                                # if str(io_call).startswith("write(6,"):
                                #     begin_char="\\33[?25l" #输入字符前面字段长度
                                #     char=char[len(begin_char)]#取出输入的字符
                                #     output_str+=char

                        else:  # 正常命令下

                            if char == "\\r":  # 回车换行
                                print(output_str)
                                output_str = ""
                            elif char == "\\33[A":  # 鼠标上移
                                output_char = "[up 1]"
                            elif char == "\\33[B":  # 鼠标下移
                                output_char = "[down 1]"
                            elif char == "\\33[C":  # 鼠标右移
                                #output_char = "[right 1]"
                                if abs(right_count)<=len(output_str):
                                    right_count-=1
                            elif char == "\\33[D":  # 鼠标左移
                                #output_char = "[left 1]"
                                if left_count<=len(output_str):
                                    left_count+=1

                            elif char == "\\10":  # 回退
                                output_list=list(output_str)


                                if left_count==0 and right_count==0:
                                    output_list.pop()
                                else:
                                    output_list.pop(len(output_list)+right_count-left_count)

                                output_str="".join(output_list)

                            elif char == '\\n':
                                output_char=""
                            elif char=="\\7":#清空
                                output_str=""
                                #output_char = "清空"
                            else:
                                output_char = char
                                #print("-----",output_str)

                    # 判读是不是输入读取，后面跟有select(8:
                    if io_call == 'select(8,':
                        input_flag = True

                    # 判断是不是正常输出
                    if input_flag:
                        insert_char=output_char.strip(',').strip('"').strip()
                        if left_count==0 and right_count==0:
                            output_str += insert_char
                        else:
                            output_list=list(output_str)
                            output_list.insert(len(output_list)+right_count-left_count,insert_char)
                            output_str="".join(output_list)
                        output_char=""
                        input_flag = False


if __name__ == "__main__":
    audit_obj = AuditLogAnalysis("session_24_afbf11de-e4ef-47ee-8fd0-b3996b68fa56.log")
    audit_obj.parse()
