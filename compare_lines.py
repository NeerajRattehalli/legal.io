

no_dups = open('companiesWithSocialsNoDups.csv', 'r')
og = open('thingsToCheckManually.csv', 'r')


og_arr = og.readlines()
no_dups_arr = no_dups.readlines()

print(og_arr)
print(no_dups_arr)

print(len(og_arr))
print(len(no_dups_arr))



print("hello")

names=[]


for i in no_dups_arr:
    names.append(i.split(",")[0])
print(names)



checked_list = []

for element in names:
    if(element in checked_list):
        print(element)
    else:
        checked_list.append(element)
print(checked_list)



