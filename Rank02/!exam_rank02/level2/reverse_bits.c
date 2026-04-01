unsigned char	reverse_bits(unsigned char octet)
{
    int i = 8;
    unsigned char rev = 0;

    while (i > 0)
    {
        rev = (rev << 1) | (octet & 1);
        octet = octet >> 1;
        i--;
    }
    return rev;
}