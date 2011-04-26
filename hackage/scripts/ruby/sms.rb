require 'rubygems'
require 'celerity'

#sms.rb - command line utility to send sms via 160by2.com using celerity as headless browser
#author: Colin Thomas 
#email: colin at fafadiatech dot com
#date: 27-04-2011
#useage: $jruby sms.rb <mobile> "<message>"

browser = Celerity::Browser.new
$username = "phone_number_here"
$password = "160by2.com_password_here"

$contact = ARGV[0]
$message = ARGV[1]


	browser.goto("http://m.160by2.com")
	browser.text_field(:id => "txtUserName").set $username.to_s()
	browser.text_field(:id => "txtPasswd").set $password.to_s()
	browser.button(:id => "cmdSubmit").click

	browser.link(:text => "Compose").click

	browser.text_field(:name => "txt_mobileno").set $contact.to_s()
	browser.text_field(:name => "txt_msg").set $message.to_s()
	browser.button(:id => "cmdSend").click

	if browser.text.include? "Successfully"
		puts "Message sent successfully to " + $contact.to_s()
	else
		puts "ERROR"
	end


browser.link(:text => "Logoff").click
browser.close