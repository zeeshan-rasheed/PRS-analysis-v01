def sort_tsv(input_file, output_file):
    with open(input_file, 'r') as f:
        header = None
        data = []
        for line in f:
            if line.startswith('#CHROM'):
                header = line
            elif not line.startswith('##'):
                data.append(line.strip().split('\t'))
        data.sort(key=lambda row: row[1])

    with open(output_file, 'w') as f:
        if header:
            f.write(header)
        for row in data:
            f.write('\t'.join(row) + '\n')

def insert_data(data: str, index: int, line: str) -> str:
    elements = line.split('\t')
    elements.insert(index, data)
    return '\t'.join(elements)

input_ma = "C:/Users/ZRasheed/Desktop/OVerelaping Project/Genotype_combine_data/chr22.seq.vcf"
input_ma_sorted = "C:/Users/ZRasheed/Desktop/OVerelaping Project/Genotype_combine_data/Sorted File/chr22.seq.vcf_files"

input_wes = "/C:/Users/ZRasheed/Desktop/OVerelaping Project/Genotype_combine_data/chr22.exome.vcf"
input_wes_sorted = "C:/Users/ZRasheed/Desktop/OVerelaping Project/Genotype_combine_data/Sorted File/sorted_chr22.exome.vcf"

output_vcf = "C:/Users/ZRasheed/Desktop/OVerelaping Project/Genotype_combine_data/Mergerfile/chr22_merged.vcf"

test_1 = 'C:/Users/ZRasheed/Desktop/OVerelaping Project/Genotype_combine_data/Test/test_123.csv'
test_2 = 'C:/Users/ZRasheed/Desktop/OVerelaping Project/Genotype_combine_data/Test/test_245.csv'

input_wes_sorted, input_wes = test_2, test_2
input_ma_sorted, input_ma= test_1, test_1
# sort_tsv(input_ma, input_ma_sorted)

# Read MA
sample_ids_ma = []
with open(input_ma, "r") as ma_file:
    for line in ma_file:
        if line.startswith('#CHROM'):
            fields = line.strip().split('\t')
            sample_ids_ma = fields[9:]
            break

# Read WES
# sort_tsv(input_wes, input_wes_sorted)

sample_ids_wes = []
with open(input_wes, "r") as wes_file:
    for line in wes_file:
        if line.startswith('#CHROM'):
            fields = line.strip().split('\t')
            sample_ids_wes = fields[9:]
            break

common_samples = set(sample_ids_ma) & set(sample_ids_wes)
extra_samples = set(sample_ids_wes).difference(common_samples)

# def merge_vcf(input_wes_sorted, input_ma_sorted, output_vcf):
with open(output_vcf, "w") as output_file:

    for sample_id in common_samples:
        with open(input_wes_sorted, "r") as wes_file, open(input_ma_sorted, "r") as ma_file:
            sample_index_wes = sample_ids_wes.index(sample_id)            
            sample_index_ma = sample_ids_ma.index(sample_id)
            written_pos = []
            for i, line_wes in enumerate(wes_file):
                if line_wes.startswith('#CHROM'):
                    continue                        
                fields_wes = line_wes.strip().split('\t')
                pos_wes = fields_wes[1]
                data_wes = fields_wes[sample_index_wes]
                for j, line_ma in enumerate(ma_file):
                    if line_ma.startswith('#CHROM'):
                        continue
                    fields_ma = line_ma.strip().split('\t')
                    pos_ma = fields_ma[1]
                    if pos_wes >= pos_ma and pos_ma not in written_pos:
                        output_file.write(line_ma)
                        written_pos.append(pos_ma)
                        print(written_pos)                        
                if pos_wes not in written_pos:
                    if pos_wes > pos_ma:
                        output_file.write(line_ma)
                        written_pos.append(pos_ma)
                        print(written_pos)          
                    print('line_res')
                    line_result = '\t'.join(fields_wes[:9])                            
                    line_result += insert_data(data_wes, sample_index_ma, line_ma[9:])
                    output_file.write(line_result)
                    written_pos.append(pos_wes)
                    print(written_pos)
