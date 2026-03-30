unsigned char	reverse_bits(unsigned char octet)
{
    int i = 8;
    unsigned char rev = 0;

    while (i > 0)
    {
        rev = (rev * 2) + (octet % 2);
        octet = octet / 2;
        i--;
    }
    return rev;
}