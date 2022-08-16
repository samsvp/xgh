require "date"

def find_nth_weekday_date(target_n, week_day, t_date)
    n = 0 # counter of times we hit the target day
    one_day = 60 * 60 * 24
    for i in 0..31 do
        if t_date.wday == week_day then
            # if we hit the target number then return
            if n == target_n then return t_date end
            # else increment our target counter
            n += 1
        end
        
        t_date += one_day # add one day to our date
    end

    return t_date
end


def find_last_weekday_date(week_day, t_date)
    one_day = 60 * 60 * 24
    r_date = t_date
    for i in 0..31 do
        # if the current day is the target day store it
        if t_date.wday == week_day then r_date = t_date end
        t_date += one_day
    end

    # return the last date where we hit the target week day
    return r_date
end


def find_teenth_weekday_date(desc, t_date)
    one_day = 60 * 60 * 24
    weekteenth_to_num = ["sunteenth", "monteenth", "tuesteenth", "wednesteenth", 
        "thursteenth", "friteenth", "saturteenth"]

    w = weekteenth_to_num.index(desc)
    
    if w == nil then return t_date end

    for i in 0..31 do
        # return on the first weekday that is in a day that ends eith "teen"
        if t_date.day >= 13 && t_date.wday == w then return t_date end
        t_date += one_day
    end
end


def meetup(date_desc)
    # expects sentences in the following manner
    # "The sunteenth of January 2017"
    # "The second Monday of January 2017"
    # the input is case insensitive
    desc_to_number = ["first", "second", "third", "fourth", "fifth"]
    weekday_to_num = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]


    arr = date_desc.downcase.split
    desc = arr[1]
    week_day = weekday_to_num.index(arr[2])
    month, year = arr.last(2)
    t_date = Date.parse("#{month} #{year}").to_time

    target_n = desc_to_number.index(desc)
    if week_day != nil && target_n != nil then
        return find_nth_weekday_date(target_n, week_day, t_date)
    end

    if desc == "last" then
        return find_last_weekday_date(week_day, t_date)
    end

    return find_teenth_weekday_date(desc, t_date)
end


date = Date.parse("January 2017").to_time

t = meetup("The sunteenth of January 2017")
puts t
puts t.wday
puts date