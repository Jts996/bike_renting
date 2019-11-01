$(document).ready(function(){
	$("#btn1").click(function(){
		alert("Password Changed Successfully");
	});

	$("#btn2").click(function(){
		alert("Account Closed Successfully");
	});

	$("#show").click(function(){
		$("#show").removeClass("far fa-eye-slash").addClass("far fa-eye");
		if($(".pwd").attr("type") === "password"){
			$("#show").removeClass("far fa-eye-slash").addClass("far fa-eye");
			$(".pwd").attr("type","text");
		}
		else{
			$("#show").removeClass("far fa-eye").addClass("far fa-eye-slash");
			$(".pwd").attr("type","password");
		}
	});

	$("#show1").click(function(){
		$("#show1").removeClass("far fa-eye-slash").addClass("far fa-eye");
		if($(".pwd").attr("type") === "password"){
			$("#show1").removeClass("far fa-eye-slash").addClass("far fa-eye");
			$(".pwd").attr("type","text");
		}
		else{
			$("#show1").removeClass("far fa-eye").addClass("far fa-eye-slash");
			$(".pwd").attr("type","password");
		}
	});

	$("#show2").click(function(){
		$("#show2").removeClass("far fa-eye-slash").addClass("far fa-eye");
		if($(".pwd").attr("type") === "password"){
			$("#show2").removeClass("far fa-eye-slash").addClass("far fa-eye");
			$(".pwd").attr("type","text");
		}
		else{
			$("#show2").removeClass("far fa-eye").addClass("far fa-eye-slash");
			$(".pwd").attr("type","password");
		}
	});
});

