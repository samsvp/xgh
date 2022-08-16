def microwave_time(time)
    # the number of minutes is the integer division of the time by 60
    minutes = time / 60
    # the number of seconds is the remainder of the divison of time by 60
    seconds = time % 60
    # add a 0 before the number if it has only one digit
    minutes_string =  minutes < 10? "0#{minutes}" : "#{minutes}"
    seconds_string =  seconds < 10? "0#{seconds}" : "#{seconds}"
    return "#{minutes_string}:#{seconds_string}"
end


puts microwave_time(90)
puts microwave_time(60)
puts microwave_time(120)
puts microwave_time(125)