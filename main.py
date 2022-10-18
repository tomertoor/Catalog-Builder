import mitreattack.attackToExcel.attackToExcel as attackToExcel
import mitreattack.attackToExcel.stixToDf as stixToDf

# download and parse ATT&CK STIX data
data = attackToExcel.get_stix_data("enterprise-attack")
# get Pandas DataFrames for techniques
techniques_data = stixToDf.techniquesToDf(data, "enterprise-attack") 

techniques_df = techniques_data["techniques"]

print("Tactics list: \n", stixToDf.tacticsToDf(data)["tactics"].sort_values("ID"))
technique = input("Enter technique ID:")

technique = techniques_df[techniques_df["ID"].str.contains(technique)]["name"].tolist()
print("Technqiue name: ", technique[0])
for sub_technique in technique[1:]:
    print("Sub-technique: ", sub_technique)