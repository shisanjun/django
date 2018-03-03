/**
 * Created by Administrator on 2017/11/6.
 */

/*增加主机组*/
$("#hostgroup_add").click(
    function(){
        $(".shade,.hostgroup_add_div").removeClass("hide");
    }
)
/*主机组修改ajax显示层*/
$(".show_div").on("click","#close_div",
    function(){
        $(".shade,.show_div").addClass("hide");
    }
)
/*主机组删除ajax显示层*/
$(".hostgroup_edit_a").click(
    function(){
         $(".shade,.hostgroup_edit_div").removeClass("hide");
        var gid=$(this).parent().parent().attr("gid");
        var name=$(this).parent().prev().text();

        $('.hostgroup_edit_div input[name="gid"]').val(gid);
        $('.hostgroup_edit_div #groupname').val(name);
    }

)
/*主机组ajax修改保存*/
$("#hostgroup_edit_mode").click(
        function () {
            $.ajax(
                    {
                        url: "/machine/hostgroup_edit",
                        type: "post",
                        dataType: 'JSON',
                        data: $("#hostgroup_edit_form").serialize(),
                        success: function (data) {

                            if (data.status) {
                                location.reload();
                            }
                            else {
                                alert("123");
                            }
                        }
                    }
            );
        }
)
/*主机组ajax删除功能*/
$(".hostgroup_delete_a").click(
    function(){
        console.log($(this).parent())
        $.ajax({
            url:"/machine/hostgroup_delete",
            type:"post",
            dataType: 'JSON',
            data:{"gid":$(this).parent().parent().attr("gid")},
            success:function(data){
                if (data.status) {
                    location.reload();}
                else {
                    alert("error")
                }

            }
        });
    }

)

/*主机组修改ajax显示层*/
$("#user_add").click(
    function(){
        $(".shade,.user_add_div").removeClass("hide");
    }
)

/*用户修改显示层*/

$(".user_edit_a").click(
    function(){
        $(".shade,.user_edit_div").removeClass("hide");
        //获取用户数据

        $(this).parent().prevAll("td[target]").each(
            function(){
                var flag=$(this).attr("target");
                var val=$(this).text();
                var tmp='#user_edit_form input[name="'+flag+'"]';
                $(tmp).attr("value",val)
            }
        )
        var gid=$(this).parent().prevAll("td[td_gid]").attr("td_gid")

        var tmp1='#user_edit_form option[value="'+gid+'"]';

        $(tmp1).prop("selected",true)
    }
)
/*用户修改ajax保存*/
$("#user_edit_mode").click(
    function(){
        $.ajax({
            url:"/machine/user_edit",
            type:"post",
            dataType:"JSON",
            data:$("#user_edit_form").serialize(),
            success:function(data){
                if (data.status){
                    location.reload()
                }
            }

        })
    }
)

/*用户ajax实现删除*/

$(".user_delete_a").click(
    function(){
        $.ajax({
            url:"/machine/user_delete",
            type:"post",
            dataType:"JSON",
            data:{"uid":$(this).parent().prevAll('td[target="id"]').text()},
            success:function(data){
                if (data.status){
                    location.reload()
                }
            }
        })
    }
)

/*显示增加角色层*/
$("#usergroup_add").click(
    function(){
         $(".shade,.usergroup_add_div").removeClass("hide");
    }
)

$(".usergroup_edit_a").click(
    function(){
        $(".shade,.usergroup_edit_div").removeClass("hide");
    }
)