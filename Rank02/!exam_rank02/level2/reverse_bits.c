unsigned char	reverse_bits(unsigned char octet)
{
    int i = 8;
    unsigned char rev;

    while (i--)
    {
        rev = (rev << 1) | (octet & 1);
        octet = octet >> 1;
    }

    return rev;
}