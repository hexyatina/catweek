const TableComponent = ({data = []}) => {
    if (!data.length) return <div>No data</div>;

    const headers = Object.keys(data[0]);

    return (
        <table className="border">
            <thead className="border">
            <tr className="border">
                {headers.map(header => (
                    <th key={header} className="border">{header}</th>
                ))}
            </tr>
            </thead>

            <tbody className="border">
            {data.map((item, rowIndex) => (
                <tr key={rowIndex} className="border">
                    {headers.map((header) => (
                        <td key={header} className="border">
                            {item[header]}
                        </td>
                    ))}
                </tr>
            ))}
            </tbody>
        </table>
    )
}

export default TableComponent