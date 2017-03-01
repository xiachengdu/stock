<?php 
    header("content-type:text/html;charset=utf-8");
    //总共约1.4s
    
    $conf_array = (parse_ini_file("/config/config.ini"));
    $stock_code = $conf_array["stock_code"];
    //调用Python脚本,约0.3s
    $cmd = system("python fetch_data.py",$ret);
    //echo("ret is $ret  ");

    //连接MySQL取数据,约1s
	$conn=mysql_connect("60.205.207.56:3306","rht102","rht102");
	mysql_select_db("stock");
	mysql_query("set names utf8");
	$sql = "select * from stocks_data where stock_code = \"{$stock_code}\"";
	$rst = mysql_query($sql);
	$result_row = mysql_num_rows($rst);
	if($result_row == 0){
		echo "空";
	}else{
		while($row = mysql_fetch_assoc($rst)) {
		echo "{$row['stock_code']}<br>";
		echo "{$row['stock_name']}<br>";
		echo "<font color=\"blue\">{$row['price_yesterday']}</font><br>";
		echo "{$row['price_open']}<br>";
		echo "<font color=\"red\">{$row['price']}</font><br>";
		echo "{$row['count_time']}<br>";
		echo "{$row['turnover_volume']}<br>";
		echo "{$row['turnover_amount']}<br>";
		echo "{$row['float_persent']}<br>";
		}
	}
?>

<?php 
//<!--JS 页面自动刷新 -->
echo ("<script type=\"text/javascript\">");
echo ("function fresh_page()");    
echo ("{");
echo ("window.location.reload();");
echo ("}"); 
echo ("setTimeout('fresh_page()',1000);");      
echo ("</script>");
?>