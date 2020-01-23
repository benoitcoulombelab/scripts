import logging
import os

import click


@click.command()
@click.option('--input', '-i', type=click.Path(exists=True), default='sequences.txt', show_default=True,
              help='Sequences for each samples.')
@click.option('--output', '-o', type=click.Path(), default='sequences-out.txt', show_default=True,
              help='Output compatible with Perseus.')
def main(input, output):
    '''Converts sequences per samples into a format compatible with Perseus.'''
    logging.basicConfig(filename='sequences2perseus.log', level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    sequences = read_sequences(input)
    matrix = generate_matrix(sequences)
    write_matrix(matrix, output)


def read_sequences(input):
    '''Reads all sequences from input.'''
    sequences = {}
    with open(input, 'r') as infile:
        line = infile.readline()
        samples = line.rstrip('\r\n').split('\t')
        sequences = {sample : [] for sample in samples}
        for line in infile:
            columns = [seq.replace(' ', '') for seq in line.rstrip('\r\n').split('\t')]
            for i in range(0, len(columns)):
                if columns[i]:
                    sequences[samples[i]].append(columns[i])
    return sequences


def generate_matrix(sample_sequences):
    '''Generates Perseus matrix base on samples' sequences.'''
    headers = ['Sequence']
    headers.extend(list(sample_sequences.keys()))
    matrix = [headers]
    sequences = list(set().union(*[sample_sequences[sample] for sample in sample_sequences]))
    for i in range(0, len(sequences)):
        sequence = sequences[i]
        matrix.append([sequence])
        for sample in sample_sequences:
            matrix[i + 1].append(1 if sequence in sample_sequences[sample] else 0)
    return matrix


def write_matrix(matrix, output):
    '''Writes matrix to output file'''
    with open(output, 'w') as outfile:
        for columns in matrix:
            outfile.write('\t'.join([str(col) for col in columns]))
            outfile.write('\n')
        

if __name__ == '__main__':
    main()
