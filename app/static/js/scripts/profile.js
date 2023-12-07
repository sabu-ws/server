// Enable 2FA
$("#enable2fa").click(function(){	
	$.ajax({
		type: "GET",
		url: otp_url,
		success: function(data)
		{
			$("#otp_url").val(data);
			$("#qrcode_render").attr('src',qrcode_url+"?url="+data);
		}
	});
});

// Check TOTP Code
$("#FormCheckTotp").submit(function(e){
	e.preventDefault();
	if($("#TestTOTPCodeInput").val()==""){
		$("#ErrorTotp").attr("style","");
		$("#ErrorTotpMSG").html("Please enter your code.");
	}else{
		$.ajax({
			type: "POST",
			url: check_otp_url,
			data: $(this).serialize(),
			success: function(data)
			{
				if(data=="ok"){
					window.location.reload();
				}else{
					$("#ErrorTotp").attr("style","");
					$("#ErrorTotpMSG").html(data);
				}
			}
		});
	}
});
$("#otpLinkBtn").click(function(){
	$("#otp_url").select();
	document.execCommand('copy');
	$("#copyInfoText").html("Copied ✓")
	window.getSelection().removeAllRanges();
});