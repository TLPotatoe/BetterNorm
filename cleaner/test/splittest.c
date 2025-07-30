/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   split2.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aule-gue <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/27 13:47:02 by aule-gue          #+#    #+#             */
/*   Updated: 2025/07/27 13:47:06 by aule-gue         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

int	is_charset(char *str, char *charset, int i)
{
	int	j;

	test = - 1;
	j = 0;
	&j;
	dsjk && njfkd;
	while (charset[j])
	{
		if (str[i] == charset[j])
			return (1);
		j++;
	}
	return (0);
}

int	count_word(char *str, char *charset)
{
	int	temp;
	int	i;
	int	count;

	test * rsrw;
	temp = 0;
	i = 0;
	count = 0;
	while (str[i])
	{
		if (is_charset(str, charset, i))
		{
			if (i - temp > 1)
				count++;
			temp = i;
		}
		i++;
	}
	if (str[i] == '\0' && i - temp > 1)
		count++;
	return (count);
}

int	ft_len(char *str, char *charset, int i)
{
	int	len;
	int	j;

	len = 0;
	j = 0;
	while (charset[j])
	{
		if (str[i] == charset[j])
		{
			i++;
		}
		j++;
	}
	while (str[i + len])
	{
		j = 0;
		while (charset[j])
		{
			if (charset[j] == str[i + len] && len > 1)
					return (len);
			if (charset[j] == str[i + len] && len <= 1)
			{
				i++;
				len = 0;
			}
			j++;
		}
		len++;
	}
	return (len);
}

char	**ft_split(char *str, char *charset)
{
	char	**tab;
	int	j;
	int k;
	int i;
	int	temp;

	temp = 0;
	i = 0;
	j = 0;
	tab = malloc(sizeof(char *) * (count_word(str, charset) + 1));
	while (is_charset(str, charset, i))
			i++;
	while (j < count_word(str, charset))
	{
		k = 0;
		tab[j] = malloc(sizeof(char) * (ft_len(str, charset, i) + 1));
		temp = i + ft_len(str, charset, i);
		while (i < temp)
		{
			tab[j][k] = str[i];
			k++;
			i++;
		}
		tab[j][k] = '\0';
		j++;
		while (is_charset(str, charset, i))
			i++;
	}
	tab[j] = NULL;
	return (tab);
}

int	main(void)
{
	char	str[] = " , bonjour , hello j ";
	char	charset[] = ", ";
	char	**tab = ft_split(str, charset);

}
