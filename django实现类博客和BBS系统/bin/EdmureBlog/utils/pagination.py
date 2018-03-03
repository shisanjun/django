__author__ = 'Administrator'
from django.utils.safestring import mark_safe

class Page:

    def __init__(self,current_page,data_count,per_page_count=10,pager_num=7):
        self.current_page = current_page
        self.data_count = data_count
        self.per_page_count = per_page_count
        self.pager_num = pager_num
    @property
    def start(self):
        return (self.current_page-1) * self.per_page_count
    @property
    def end(self):
        return self.current_page * self.per_page_count

    @property
    def total_count(self):
        v,y = divmod(self.data_count, self.per_page_count)
        if y:
            v += 1
        return v

    def page_str(self, base_url):
        page_list = []

        if self.total_count < self.pager_num:
            start_index = 1
            end_index = self.total_count + 1
        else:
            if self.current_page <= (self.pager_num+1)/2:
                start_index = 1
                end_index = self.pager_num + 1
            else:
                start_index = self.current_page - (self.pager_num-1)/2
                end_index = self.current_page + (self.pager_num+1)/2
                if (self.current_page + (self.pager_num-1)/2) > self.total_count:
                    end_index = self.total_count + 1
                    start_index = self.total_count - self.pager_num + 1

        if self.current_page == 1:
            prev = '<li><a  href="javascript:void(0);">上一页</a></li>'
        else:
            prev = '<li><a  href="%s?p=%s">上一页</a></li>' %(base_url,self.current_page-1,)
        page_list.append(prev)

        for i in range(int(start_index),int(end_index)):
            if i ==self.current_page:
                temp = '<li><a  href="%s?p=%s">%s</a></li>' %(base_url,i,i)
            else:
                temp = '<li><a  href="%s?p=%s">%s</a></li>' %(base_url,i,i)
            page_list.append(temp)

        if self.current_page == self.total_count:
            nex = '<li><a href="javascript:void(0);">下一页</a></li>'
        else:
            nex = '<li><a  href="%s?p=%s">下一页</a></li>' %(base_url,self.current_page+1,)
        page_list.append(nex)

        jump = """

        <li><input id="go_page_num" type='text'
        style="width:45px;height:32px;padding:2px 5px;margin:0px 10px 0px 2px;" placeholder="页码"/></li>
        <li><a onclick='jumpTo(this,"%s?p=");'>跳转</a></li>
        <script>
            function jumpTo(ths,base){
                var val = ths.previousSibling.value;
                //var val =document.getElementById("id").value;
                console.log(val)
                location.href = base + val;
            }
        </script>
        """ %(base_url,)

        page_list.append(jump)

        page_str = mark_safe("".join(page_list))

        return page_str