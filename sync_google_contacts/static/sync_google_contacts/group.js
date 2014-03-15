		$(document).ready(function () {
			$('#GroupMngt').jtable({
			title: 'Manage groups',
			paging: false, //Enable paging
			pageSize: 10, //Set page size (default: 10)
			sorting: true, //Enable sorting
			create: true,
			edit:false,
			defaultSorting: 'Id DESC', //Set default sorting
			actions: {
				listAction: '/groupmanagement/ajax/group-m/display/',
				createAction: '/groupmanagement/ajax/group-m/add/',
				updateAction: '/groupmanagement/ajax/group-m/update/',
				deleteAction: '/groupmanagement/ajax/group-m/delete/'
			},
			fields: {
				'Id': {
				key: true,
				list: false,
				create: false,
				hidden: true,
				},

                Users: {
                    title: '',
                    width: '5%',
                    sorting: false,
                    edit: false,
                    create: false,
                    display: function (userData) {
                        //Create an image that will be used to open child table
						html = '<img src="'+STATIC_URL+'group_user_mngt/contact-list-icon.png">';
                        var $img = $(html);
                        //Open child table when user clicks the image
                        $img.click(function () {
                            $('#GroupMngt').jtable('openChildTable',
                                    $img.closest('tr'),
                                    {
                                        title: userData.record.name + ' - Attached users',
										sorting: true,
                                        actions: {
                                            listAction: '/groupmanagement/ajax/user-s/display/'+userData.record.name,
                                            deleteAction: '/groupmanagement/ajax/user-s/delete/'+userData.record.name,
                                            createAction: '/groupmanagement/ajax/user-s/add/'+userData.record.name
                                        },
                                        fields: {
                                            'Id': {
												key: true,
                                                list: false,
												create: false,
												hidden: true,
                                            },
                                            'name': {
												title : 'user name',
                                                key: false,
                                                edit: false,
												create: true,
												display: function (data) { return data.record.name;},
												options: function (data) {
													data.clearCache()
													return '/groupmanagement/ajax/user-s/index/'+userData.record.name ; }
                                            },
                                            'email': {
												title : 'email',
                                                key: false,
                                                edit: false,
												create: false,
												display: function (data) { return data.record.email;},
                                            },
                                            'lastname': {
												title : 'last name',
                                                key: false,
												edit: false,
												create: false,
                                            },
                                            'is_active': {
												title : 'is active',
                                                key: false,
												edit: false,
												create: false,
												type: 'checkbox',
												values: { 'false': 'Not active', 'true': 'Active' },
                                            },
                                            'is_staff': {
												title : 'is staff',
                                                key: false,
												edit: false,
												create: false,
												type: 'checkbox',
												values: { 'false': 'No', 'true': 'Yes' },
                                            },
                                            'is_superuser': {
												title : 'is superuser',
                                                key: false,
												edit: false,
												create: false,
												type: 'checkbox',
												values: { 'false': 'No', 'true': 'Yes' },
                                            },
                                            'firstname': {
												title : 'firstname',
                                                key: false,
												edit: false,
												create: false,
                                            },
	                                        'last_login': {
	                                            title: 'last login',
	                                            width: '30%',
												edit: false,
												create: false,
											},
	                                        'date_joined': {
	                                            title: 'date joined',
	                                            width: '30%',
												edit: false,
												create: false,
											},
                                        }
                                    }, function (data) { //opened handler
                                        data.childTable.jtable('load');
                                    });
                        });
                        //Return image to show on the person row
                        return $img;
                    }
                },

				'name': {
				title: 'group name',
				edit: true,
				width: '20%'
				},
			}
			});
		$('#GroupMngt').jtable('load');
		});
